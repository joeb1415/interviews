import json
import logging
import pandas as pd
from pandas.io.json import json_normalize

# TODO: separate this into a logging module to log to file in a production app
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class DoctorData:
    """
    A "Doctor" is uniquely defined by a [First name, Last name] pair, or by a NPI
    A "Practice" is uniquely defined by an address
    Some doctors have multiple practices.
    The "Practice" DataFrames are slightly de-normalized to include the doctor info, rather than simply a "Doctor ID".
    This is to streamline processing the data as presented in the source files. A database model would normalize these.
    """

    def __init__(self, valid_doctors=None, valid_practice=None, test_doctors=None, test_practices=None):
        self.doctor_cols = ['first_name', 'last_name', 'npi']
        self.practice_cols = ['first_name', 'last_name', 'npi', 'street', 'street_2', 'city', 'state', 'zip']
        self.valid_doctors = valid_doctors
        self.valid_practices = valid_practice
        self.test_doctors = test_doctors
        self.test_practices = test_practices

        self.matched_practices = pd.DataFrame()
        self.new_practices = pd.DataFrame()
        self.mismatched_npi = pd.DataFrame()
        self.mismatched_name = pd.DataFrame()
        self.new_doctors = pd.DataFrame()

    def read_validated_data_json(self, filepath):
        logging.debug('Begin importing validated data set')

        doctor_col_map = {'doctor.' + field: field for field in self.doctor_cols}

        with open(filepath, 'r') as f:
            lines = f.readlines()

            # the input file is a line-separated list of json objects.
            # To use available libraries, I'll format this as a proper json list instead.
            full_json_str = '[{body}]'.format(
                body=','.join(lines)
            )
            validated_json = json.loads(full_json_str)

        # get list of 11,231 validated doctors. Fix their column names
        self.valid_doctors = json_normalize(validated_json)
        self.valid_doctors = self.valid_doctors.rename(columns=doctor_col_map)
        self.valid_doctors = self.valid_doctors[self.doctor_cols]

        # get list of 22,443 validated practices. Fix their column names
        self.valid_practices = json_normalize(
            validated_json,
            'practices',
            [['doctor', 'first_name'], ['doctor', 'last_name'], ['doctor', 'npi']]
        )
        self.valid_practices = self.valid_practices.rename(columns=doctor_col_map)

        logging.debug('Completed importing validated data set')

    def read_match_data_csv(self, filepath):
        logging.debug('Begin importing non-validated data set')

        self.test_practices = pd.read_csv(filepath)
        self.test_doctors = self.test_practices[self.doctor_cols].drop_duplicates()

        logging.debug('Completed importing non-validated data set')

    def evaluate_new_data_set(self, valid_doctors, test_doctors, valid_practices, test_practices):
        test_practices = self._check_matched_practices(valid_practices, test_practices)
        test_practices = self._check_new_practices(valid_doctors, test_practices)
        test_practices = self._check_mismatched_npi(valid_doctors, test_doctors, test_practices)
        test_practices = self._check_mismatched_name(valid_doctors, test_doctors, test_practices)

        # Remaining test rows may be new doctors, or may be errors from the 3rd party
        self.new_doctors = test_practices

    def _check_matched_practices(self, valid_practices, test_practices):
        """
        1. Which of the new rows match validated rows.
        Note: Turned out to be 0 in the sample test set.
        """
        self.matched_practices = pd.merge(
            valid_practices, test_practices,
            on=self.practice_cols
        )[self.practice_cols]

        # Remove matched rows
        test_practices = pd.merge(
            test_practices, self.matched_practices,
            how='left', on=self.practice_cols, indicator=True
        )
        test_practices = test_practices[test_practices['_merge'] == 'left_only'][self.practice_cols]
        return test_practices

    def _check_new_practices(self, valid_doctors, test_practices):
        """
        2. Which might be new practices of existing doctors
        TODO: check for mis-entries in address data (i.e. typo in street name, otherwise matching)
        """
        self.new_practices = pd.merge(
            valid_doctors, test_practices,
            on=self.doctor_cols
        )[self.practice_cols]

        # Remove matched rows
        test_practices = pd.merge(
            test_practices, self.new_practices,
            how='left', on=self.practice_cols, indicator=True
        )
        test_practices = test_practices[test_practices['_merge'] == 'left_only'][self.practice_cols]
        return test_practices

    def _check_mismatched_npi(self, valid_doctors, test_doctors, test_practices):
        """
        3a. Mis-matched NPI
        """
        self.mismatched_npi = pd.merge(
            valid_doctors, test_doctors,
            on=['first_name', 'last_name'], suffixes=['_valid', '_test']
        )
        self.mismatched_npi = self.mismatched_npi[
            (self.mismatched_npi['npi_valid'] != self.mismatched_npi['npi_test'])
        ]
        self.mismatched_npi = self.mismatched_npi.rename(columns={'npi_test': 'npi'})

        # Remove matched rows
        test_practices = pd.merge(
            test_practices, self.mismatched_npi,
            how='left', on=self.doctor_cols, indicator=True
        )
        test_practices = test_practices[test_practices['_merge'] == 'left_only'][self.practice_cols]
        return test_practices

    def _check_mismatched_name(self, valid_doctors, test_doctors, test_practices):
        """
        3b. Mis-matched name
        Note: Turned out to be 0 in the sample test set.
        """
        self.mismatched_name = pd.merge(
            valid_doctors, test_doctors,
            on=['npi'], suffixes=['_valid', '_test']
        )
        self.mismatched_name = self.mismatched_name[
            (self.mismatched_name['first_name_valid'] != self.mismatched_name['first_name_test']) |
            (self.mismatched_name['last_name_valid'] != self.mismatched_name['last_name_test'])
        ]
        self.mismatched_name = self.mismatched_name.rename(
            columns={'first_name_test': 'first_name', 'last_name_test': 'last_name'}
        )

        # Remove matched rows
        test_practices = pd.merge(
            test_practices, self.mismatched_name,
            how='left', on=self.doctor_cols, indicator=True
        )
        test_practices = test_practices[test_practices['_merge'] == 'left_only'][self.practice_cols]
        return test_practices

    def print_result(self):
        message = '''
Given validated data set of {valid_data_length} practices, and a test data set of {test_data_length}, we found:
1. {matched_practices} practices from the test set already in the validated set
2. {new_practices} apparent new practices of existing validated doctors
3. {mismatched_npi} test doctor name entries with missing or mismatched NPI
4. {mismatched_name} test NPI entries with mismatched doctor name vs. the validated data
5. {new_doctors} apparent new doctors

The apparent new practices and new doctors will need to be confirmed before added to the validated data set. 
        '''
        logging.debug(
            message.format(
                valid_data_length=self.valid_practices.shape[0],
                test_data_length=self.test_practices.shape[0],
                matched_practices=self.matched_practices.shape[0],
                new_practices=self.new_practices.shape[0],
                mismatched_npi=self.mismatched_npi.shape[0],
                mismatched_name=self.mismatched_name.shape[0],
                new_doctors=self.new_doctors.shape[0]
            )
        )

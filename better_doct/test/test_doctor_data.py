import unittest
import pandas as pd
from doctor_data import DoctorData


class TestDoctorData(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDoctorData, self).__init__(*args, **kwargs)

        self.valid_doctors = pd.DataFrame(
            {
                'first_name': {0: 'Alice', 1: 'Bob', 2: 'Charlie', 3: 'Dan', 4: 'Eve'},
                'last_name': {0: 'Anderson', 1: 'Bush', 2: 'Cunningham', 3: 'Delta', 4: 'Ewing'},
                'npi': {0: '0', 1: '1', 2: '2', 3: '3', 4: '4'}
            }
        )
        self.valid_practices = pd.DataFrame(
            {
                'first_name': {0: 'Alice', 1: 'Bob', 2: 'Charlie', 3: 'Dan', 4: 'Eve'},
                'last_name': {0: 'Anderson', 1: 'Bush', 2: 'Cunningham', 3: 'Delta', 4: 'Ewing'},
                'npi': {0: '0', 1: '1', 2: '2', 3: '3', 4: '4'},
                'street': {0: '0 A', 1: '1 B', 2: '2 C', 3: '3 D', 4: '4 D'},
                'street_2': {0: 'Apt. 0', 1: 'Apt. 1', 2: 'Apt. 2', 3: 'Apt. 3', 4: 'Apt. 4'},
                'city': {0: 'Atlanta', 1: 'Boston', 2: 'Chicago', 3: 'Detroit', 4: 'Eastville'},
                'state': {0: 'AA', 1: 'BB', 2: 'CC', 3: 'DD', 4: 'EE'},
                'zip': {0: '00000', 1: '11111', 2: '22222', 3: '33333', 4: '44444'},
                'lat': {0: '80', 1: '81', 2: '82', 3: '83', 4: '84'},
                'lon': {0: '90', 1: '91', 2: '92', 3: '93', 4: '94'}
            }
        )
        self.test_doctors = pd.DataFrame(
            {
                'first_name': {0: 'Alice', 1: 'Bob', 2: 'Charlie', 3: 'Dan', 4: 'Eve'},
                'last_name': {0: 'Anderson', 1: 'Bush', 2: 'Cunningham', 3: 'Delta', 4: 'Ewing'},
                'npi': {0: '0', 1: '1', 2: '2', 3: '3', 4: '4'}
            }
        )
        # 0 is identical to valid
        # 1 has matching doctor, new address
        # 2 has mismatched doctor NPI
        # 3 has mismatched doctor name
        # 4 is new name, NPI, and address
        self.test_practices = pd.DataFrame(
            {
                'first_name': {0: 'Alice', 1: 'Bob', 2: 'Charlie', 3: 'Dan', 4: 'Eve'},
                'last_name': {0: 'Anderson', 1: 'Bush', 2: 'Cunningham', 3: 'Delta__new__', 4: 'Ewing__new__'},
                'npi': {0: '0', 1: '1', 2: '2__new__', 3: '3', 4: '4__new__'},
                'street': {0: '0 A', 1: '1 B __new__', 2: '2 C', 3: '3 D', 4: '4 D__new__'},
                'street_2': {0: 'Apt. 0', 1: 'Apt. 1', 2: 'Apt. 2', 3: 'Apt. 3', 4: 'Apt. 4'},
                'city': {0: 'Atlanta', 1: 'Boston', 2: 'Chicago', 3: 'Detroit', 4: 'Eastville'},
                'state': {0: 'AA', 1: 'BB', 2: 'CC', 3: 'DD', 4: 'EE'},
                'zip': {0: '00000', 1: '11111', 2: '22222', 3: '33333', 4: '44444'},
                'lat': {0: '80', 1: '81', 2: '82', 3: '83', 4: '84'},
                'lon': {0: '90', 1: '91', 2: '92', 3: '93', 4: '94'}
            }
        )

        self.doctor_data = DoctorData()

        self.matched_practices = pd.DataFrame()
        self.new_practices = pd.DataFrame()
        self.mismatched_npi = pd.DataFrame()
        self.mismatched_name = pd.DataFrame()
        self.new_doctors = pd.DataFrame()

    def setUp(self):
        pass

    def test_check_matched_practices(self):
        test_practices = self.doctor_data._check_matched_practices(self.valid_practices, self.test_practices)
        expected_matched_practices = pd.DataFrame(
            {
                'first_name': {0: 'Alice'},
                'last_name': {0: 'Anderson'},
                'npi': {0: '0'},
                'city': {0: 'Atlanta'},
                'lat': {0: '80'},
                'lon': {0: '90'},
                'state': {0: 'AA'},
                'street': {0: '0 A'},
                'street_2': {0: 'Apt. 0'},
                'zip': {0: '00000'}
            }
        )
        expected_test_practices = pd.DataFrame(
            {
                'first_name': {1: 'Bob', 2: 'Charlie', 3: 'Dan', 4: 'Eve'},
                'last_name': {1: 'Bush', 2: 'Cunningham', 3: 'Delta__new__', 4: 'Ewing__new__'},
                'npi': {1: '1', 2: '2__new__', 3: '3', 4: '4__new__'},
                'street': {1: '1 B __new__', 2: '2 C', 3: '3 D', 4: '4 D__new__'},
                'street_2': {1: 'Apt. 1', 2: 'Apt. 2', 3: 'Apt. 3', 4: 'Apt. 4'},
                'city': {1: 'Boston', 2: 'Chicago', 3: 'Detroit', 4: 'Eastville'},
                'state': {1: 'BB', 2: 'CC', 3: 'DD', 4: 'EE'},
                'zip': {1: '11111', 2: '22222', 3: '33333', 4: '44444'},
                'lat': {1: '81', 2: '82', 3: '83', 4: '84'},
                'lon': {1: '91', 2: '92', 3: '93', 4: '94'},
            }
        )

        # set column order
        self.doctor_data.matched_practices = self.doctor_data.matched_practices[self.doctor_data.practice_cols]
        expected_matched_practices = expected_matched_practices[self.doctor_data.practice_cols]
        test_practices = test_practices[self.doctor_data.practice_cols]
        expected_test_practices = expected_test_practices[self.doctor_data.practice_cols]

        self.assertTrue(self.doctor_data.matched_practices.equals(expected_matched_practices))
        self.assertTrue(test_practices.equals(expected_test_practices))

    def test_check_new_practices(self):
        # TODO:
        pass

    def test_check_mismatched_npi(self):
        # TODO:
        pass

    def test_check_mismatched_name(self):
        # TODO:
        pass


if __name__ == '__main__':
    unittest.main()

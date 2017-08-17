import pandas as pd


class BabyAPI:
    def __init__(self):
        self.data = pd.DataFrame()
        self.data_path = 'baby_name_data.json'  # https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-data-by-state-and-district-of-#topic=developers_navigation

    def load_data(self):
        self.data = pd.read_json(self.data_path)
        self.data = self.data.rename(columns={
            0: 'year',
            1: 'name',
            2: 'gender',
            3: 'count'
        })

    def get_freq(self, name, gender):
        """

        :param name: First name, first char caps
        :param gender: F or M or 'both'
        :return:
        {
            [
                {
                    year:
                    gender:
                    count:
                }
            ]
        }

        """
        if gender == 'both':
            data = self.data[(self.data['name'] == name)]
        else:
            data = self.data[(self.data['name'] == name) & (self.data['gender'] == gender)]

        data = data[['year', 'gender', 'count']]

        return data.to_json(orient='records')

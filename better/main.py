from doctor_data import DoctorData


def main():
    # TODO: Move settings to a config.ini type file
    valid_data_filepath = 'data_files/source_data.json'
    test_data_filepath = 'data_files/match_file.csv'

    doctor_data = DoctorData()
    doctor_data.read_validated_data_json(valid_data_filepath)
    doctor_data.read_match_data_csv(test_data_filepath)
    doctor_data.evaluate_new_data_set(
        doctor_data.valid_doctors, doctor_data.test_doctors,
        doctor_data.valid_practices, doctor_data.test_practices
    )
    doctor_data.print_result()


if __name__ == '__main__':
    main()

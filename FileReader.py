import logging
import pandas as pd


class FileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.validations = {
            'first_name': {
                'required': True,
                'first_name': None
            },
            'last_name': {
                'required': False,
                'last_name': None
            },
            'phone_number': {
                'required': True,
                'length': 9,
                'phone_number': None
            },
        }
        self.separator = {
            'required': True,
            'valid_separators': ['-', ':']
        }
        self.all_file_read = False
        self.dataframe = pd.DataFrame(columns=['first_name', 'last_name', 'phone_number'])

    def __open_file(self):
        file = None
        try:
            file = open(self.file_path, 'r')
        except FileNotFoundError as exception:
            logging.error(f"File not found. Message: {exception}")
        return file

    @staticmethod
    def __lazy_read(file):
        lines = file.readlines()
        for line in lines:
            yield line

    def __validate_and_return_values(self, line):
        validated_line = {}
        name_surname, phone_number = self.__validate_separator(line)
        if name_surname and phone_number:
            self.validations['first_name']['first_name'], self.validations['last_name']['last_name'] = \
                self.__validate_name_surname(name_surname)
            self.validations['phone_number']['phone_number'] = self.__validate_phone_number(phone_number)
            validated_line = self.__check_required_values()
        return validated_line

    def __validate_separator(self, value):
        name_surname, phone_number = None, None
        found_valid_separator = False
        for separator in self.separator['valid_separators']:
            if separator in value:
                name_surname, phone_number = value.split(separator)
                found_valid_separator = True
        if not found_valid_separator:
            logging.error(f"Separator should be in {self.separator['valid_separators']}."
                          f"Got '{value}' line")
        return name_surname, phone_number

    def __validate_name_surname(self, value):
        name, surname = None, None
        name_surname = value.rstrip()
        if ' ' in name_surname:
            name, surname = name_surname.split(' ')
        else:
            name = name_surname
        if self.validations['first_name']['required']:
            if name == ' ' or not name:
                logging.error(f"Name is required. Got '{value}' line.")
                name = None
        if self.validations['last_name']['required']:
            if surname == ' ' or not surname:
                logging.error(f"Surname is required. Got '{value}' line.")
                surname = None
        return name, surname

    def __validate_phone_number(self, value):
        phone_number = None
        raw_phone_number = value.strip()
        if raw_phone_number.isdigit() and len(raw_phone_number) == self.validations['phone_number']['length']:
            phone_number = raw_phone_number
        if self.validations['phone_number']['required']:
            if not phone_number:
                logging.error(f"Phone number is required. Got '{raw_phone_number}' line."
                              f" Phone number should be digit and contain 9 numbers")
        return phone_number

    def __check_required_values(self):
        valid_value = {}
        for key in self.validations.keys():
            if self.validations[key]['required'] and self.validations[key][key]:
                valid_value[key] = self.validations[key][key]
                self.validations[key][key] = None
            elif self.validations[key]['required'] and not self.validations[key][key]:
                self.validations[key][key] = None
                valid_value = {}
                break
            else:
                valid_value[key] = self.validations[key][key]
                self.validations[key][key] = None
        return valid_value

    def start_reading(self):
        opened_file = self.__open_file()
        if opened_file:
            file_lines = self.__lazy_read(opened_file)
            while not self.all_file_read:
                try:
                    line = next(file_lines)
                    validated_line = self.__validate_and_return_values(line)
                    if validated_line:
                        self.dataframe = self.dataframe.append(validated_line, ignore_index=True)
                except StopIteration:
                    self.all_file_read = True
                    print('Lines ended in the file')
            return self.dataframe
        else:
            return None

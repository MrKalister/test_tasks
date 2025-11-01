import csv
import re
from os import path
from typing import List

import openpyxl

DEBUG = False
REPLACE_MATCHES = {
    'mobile number': 'tel',
}


def define_path_to_file(name: str) -> str:
    return path.join(path.dirname(path.abspath(__file__)), name)


def clear_struct(name: str) -> List[str]:
    """Func for clearing structure for DB."""

    file_str = open(define_path_to_file(name)).read()
    pattern = r'\S\sDate\n\n\)|\S\sString,\n\n\s{4}\S'

    result = re.split(pattern, file_str)[:-1]
    result[0] = result[0][-4:]
    return result


def validate_date(value: str, field: str, full_name=None) -> bool:

    # Don't use \w because it include number.
    if value == '':
        result = not value
    elif full_name:
        pattern = r'^(\'|\")?[A-Z][a-z]+\s[A-Za-z]*\'?[A-Z][a-z]+(\'|\")?$'
        result = re.search(pattern, value)
    elif field == 'ssn':
        pattern = r'^\d{3}-\d{2}-\d{4}$'
        result = re.search(pattern, value)
    elif field == 'zip':
        pattern = r'^\d{5}-?\d{0,4}$'
        result = re.search(pattern, value)
    elif field == 'tel':
        pattern = r'^(\'|\")?\d?[- ]?\(?\d{3}\)?[- ]\d{3}[- ]\d{4}(\'|\")?$'
        result = re.search(pattern, value)
    elif field == 'address':
        pattern = (
            r'^(\'|\")?\d{3,5} ?[A-Z][a-z]+( [A-Z][a-z]+)*, ?[A-Z][a-z]+'
            r'( [A-Z][a-z]+)*, ?[A-Z]{2} \d{5}-?\d{0,4}|\'?(Apt. |Suite )'
            r'\d{1,5} \d{1,5} [A-Z][a-z]+( ?[A-Z][a-z]+)*, [A-Z][a-z]+ '
            r'?([A-Z][a-z]+)*, ?[A-Z]{2} \d{5}-?\d{0,4}(\'|\")?$')
        result = re.search(pattern, value)
    else:
        result = True
    return bool(result)


def append_obj(row: List[str], headers: List[str], main_struct: List[str]
               ) -> tuple[bool, str]:
    """Add result of check data and row with data in str format."""

    data_str, user_add_info = '', ''
    fields_in_main_struct, validate = [], []

    # basic data
    for index, field in enumerate(main_struct):
        full_name = re.search(r'[Ff]ullname', field)
        if full_name:
            first_name = row[headers.index('first name')]
            last_name = row[headers.index('last name')]
            value = f'\'{first_name} {last_name}\''
            fields_in_main_struct.append('first name')
            fields_in_main_struct.append('last name')
        elif field in headers:
            value = str(row[headers.index(field)])
            if any(char in value for char in (',', '\n', '"', ' ')):
                value = f'\'{value}\''
        else:
            value = ''
        validate.append(validate_date(value, field, full_name))
        # After last element haven't to be a comma.
        data_str += value + ',' if index != len(main_struct)-1 else ''
        fields_in_main_struct.append(field)

    # add info
    for field in headers:
        if field not in fields_in_main_struct:
            value = str(row[headers.index(field)])
            if any(char in value for char in (',', '\n', '"', ' ')):
                value = f'\'{value}\''
            validate.append(validate_date(value, field))
            user_add_info += f'{field}={value}|'
    # user_add_info insted of user_additional_info.
    data_str = data_str[:-1] + user_add_info + ','
    return (all(validate), data_str)


def write_csv(validate: bool, data: str) -> None:

    mode = 'a'
    if DEBUG:
        mode = 'w'
    if validate:
        file_path = 'validate_data.csv'
    else:
        file_path = 'unvalidate_data.csv'
    with open(file_path, mode, newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data, ])


def read_data(main_struct: List[str], name: str) -> None:

    book = openpyxl.load_workbook(define_path_to_file(name)).active
    headers = [
        cell.value.lower() if cell.value.lower() not in REPLACE_MATCHES
        else REPLACE_MATCHES[cell.value.lower()] for cell in book[1]]
    csv_headers = ','.join(main_struct)
    write_csv(True, csv_headers)
    write_csv(False, csv_headers)
    for row in book.iter_rows(min_row=2, values_only=True):
        validate, data = append_obj(row, headers, main_struct)
        write_csv(validate, data)


if __name__ == '__main__':
    file_with_struct = (
        input('Input the name of the file with structure:')
        or 'bl_struct.txt')
    file_for_read = (
        input('Input the name of the file you want to check:')
        or 'data.xlsx')
    main_struct = clear_struct(file_with_struct)
    read_data(main_struct, file_for_read)

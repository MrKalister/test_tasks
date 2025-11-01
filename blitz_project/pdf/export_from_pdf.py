import csv
import re
from os import path
from typing import List

import pdfplumber


DEBUG = False
REPLACE_MATCHES = {
    'email': 'usermail',
    'name': 'user_fullname',
    'date': 'dob',
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


def validate_date(value, field):

    if value == '':
        result = not value
    elif value == 'user_fullname':
        pattern = r'^(\'|\")?[A-Z][a-z]+(\'|\")?$'
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
    elif value == 'dob':
        pattern = r'^(\'|\")?\d{1,2} [A-Z][a-z]* \d{4}(\'|\")?$'
        result = re.search(pattern, value)
    elif value == 'email':
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        result = re.search(pattern, value)
    else:
        result = True
    return bool(result)


def append_obj(data: dict, main_struct: List[str]) -> tuple[bool, str]:
    """Add result of check data and row with data in str format."""

    data_str = ''
    user_add_info = ''
    fields_in_main_struct = []
    validate = []

    # basic data
    for index, field in enumerate(main_struct):
        if field in data:
            value = data[field]
            if any(char in value for char in (',', '\n', '"', ' ')):
                value = f'\'{value}\''
        else:
            value = ''
        validate.append(validate_date(value, field))
        # After last element haven't to be a comma.
        data_str += value + ',' if index != len(main_struct)-1 else ''
        fields_in_main_struct.append(field)

    # add info
    for field in data:
        if field not in fields_in_main_struct:
            value = data[field]
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
    with open(file_path, mode, newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data, ])


def extract_table_data(name):  # add type hints

    file_path = define_path_to_file(name)
    csv_headers = ','.join(main_struct)
    write_csv(True, csv_headers)
    write_csv(False, csv_headers)
    with pdfplumber.open(file_path) as pdf:
        first_page = pdf.pages[0]
        table = first_page.extract_table()
        headers, data = set(), {}
        for row in table[1:]:
            header, value = row[0], row[1]
            if header in REPLACE_MATCHES:
                header = REPLACE_MATCHES[header]
            if header in headers:
                write_csv(*append_obj(data, main_struct))
                headers = set()
                data = {}
            headers.add(header)
            data[header] = value


if __name__ == '__main__':
    file_with_struct = (
        input('Input the name of the file with structure:')
        or 'bl_struct.txt')
    file_for_read = (
        input('Input the name of the file you want to check:')
        or 'data_pdf.pdf')
    main_struct = clear_struct(file_with_struct)
    extract_table_data(file_for_read)

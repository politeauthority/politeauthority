"""Jinja Filters
"""


def format_currency(value):
    value = round(value, 2)
    value_string = str(value)
    if '.' in value_string:
        x = value_string.find('.')
        if len(value_string[x + 1:]) < 2:
            return value_string + '0'
        elif len(value_string[x + 1:]) < 1:
            return value_string + '00'
    return value_string

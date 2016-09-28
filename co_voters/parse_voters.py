"""
    Parse Voters
"""
import csv


def loc_address(row):
    __string = '%s %s %s, %s, %s %s-%s' % (
        row['HOUSE_NUM'],
        row['STREET_NAME'],
        row['STREET_TYPE'],
        row['RESIDENTIAL_CITY'],
        row['RESIDENTIAL_STATE'],
        row['RESIDENTIAL_ZIP_CODE'],
        row['RESIDENTIAL_ZIP_PLUS']
    )
    return __string


if __name__ == "__main__":
    phile = 'data/./Registered_Voters_List_Part1.txt'
    reader = csv.DictReader(open(phile), skipinitialspace=True)
    for r in reader:
        print "%s %s" % (r['FIRST_NAME'], r['LAST_NAME'])
        print loc_address(r)
        print ''

# End File: politeauthority/co_voters/parse_voters.py

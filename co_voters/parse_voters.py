"""
    Parse Voters
"""
import csv
from datetime import datetime
from politeauthority import driver_mysql


def loc_address(row):
    __string = '%s %s %s, %s, %s %s' % (
        row['HOUSE_NUM'],
        row['STREET_NAME'],
        row['STREET_TYPE'],
        row['RESIDENTIAL_CITY'],
        row['RESIDENTIAL_STATE'],
        row['RESIDENTIAL_ZIP_CODE']
    )
    if row['RESIDENTIAL_ZIP_PLUS'] not in [None, '']:
        __string += '-%s' % row['RESIDENTIAL_ZIP_PLUS']
    return __string


def format_insert(person):
    d = {}
    for x, y in person.iteritems():
        d[x.lower()] = y
    d['address_geo'] = loc_address(person)
    d['effective_date'] = __format_date(d['effective_date'])
    d['party_affiliation_date'] = __format_date(d['party_affiliation_date'])
    d['registration_date'] = __format_date(d['registration_date'])
    d['phone_num'] = __format_phone(d['phone_num'])

    sql = """INSERT INTO `voters`.`people`
        (`voter_id`, `county_code`, `county`, `last_name`, `first_name`, `middle_name`, `name_suffix`,
        `voter_name`, `status_code`, `precinct_name`, `address_library_id`, `house_num`, `house_suffix`,
        `pre_dir`, `street_name`, `street_type`, `post_dir`, `unit_type`, `unit_num`, `address_non_std`,
        `residential_address`, `residential_city`, `residential_state`, `residential_zip_code`,
        `residential_zip_plus`, `effective_date`, `registration_date`, `status`, `status_reason`,
        `birth_year`, `gender`, `precinct`, `split`, `voter_status_id`, `party`, `party_affiliation_date`,
        `phone_num`, `mail_addr1`, `mail_addr2`, `mail_addr3`, `mailing_city`, `mailing_state`,
        `mailing_zip_code`, `mailing_zip_plus`, `mailing_country`, `spl_id`, `permanent_mail_in_voter`,
        `congressional`, `state_senate`, `state_house`, `id_required`)
        VALUES ("%(voter_id)s", "%(county_code)s", "%(county)s", "%(last_name)s", "%(first_name)s",
        "%(middle_name)s", "%(name_suffix)s", "%(voter_name)s", "%(status_code)s", "%(precinct_name)s",
        "%(address_library_id)s", "%(house_num)s", "%(house_suffix)s", "%(pre_dir)s", "%(street_name)s",
        "%(street_type)s", "%(post_dir)s", "%(unit_type)s", "%(unit_num)s", "%(address_non_std)s",
        "%(residential_address)s", "%(residential_city)s", "%(residential_state)s", "%(residential_zip_code)s",
        "%(residential_zip_plus)s", "%(effective_date)s", "%(registration_date)s", "%(status)s", "%(status_reason)s",
        "%(birth_year)s", "%(gender)s", "%(precinct)s", "%(split)s", "%(voter_status_id)s", "%(party)s",
        "%(party_affiliation_date)s", "%(phone_num)s", "%(mail_addr1)s", "%(mail_addr2)s", "%(mail_addr3)s",
        "%(mailing_city)s", "%(mailing_state)s", "%(mailing_zip_code)s", "%(mailing_zip_plus)s", "%(mailing_country)s",
        "%(spl_id)s", "%(permanent_mail_in_voter)s", "%(congressional)s", "%(state_senate)s", "%(state_house)s", 
        "%(id_required)s");""" % d
    print sql
    return d


def __format_date(date_string):
    date_object = datetime.strptime(date_string, '%m/%d/%Y')
    return date_object

def __format_phone(data):
    data = str(data)
    data = data.replace('(', '')
    data = data.replace(')', '')
    data = data.replace('-', '')
    data = data.strip()
    return str(data).replace('(', '')


if __name__ == "__main__":
    phile = 'data/Registered_Voters_List_Part1.txt'
    reader = csv.DictReader(open(phile), skipinitialspace=True)
    c = 0
    thing = []
    thing_l = 0

    x = 'phone_num'.upper()
    for r in reader:
        if r[x] not in thing:
            thing.append(r[x])
        if len(r[x]) > thing_l:
            thing_1 = len(r[x])
        print "%s %s" % (r['FIRST_NAME'], r['LAST_NAME'])
        print r[x]
        print format_insert(r)
        # print r['VOTER_ID']
        # print loc_address(r)
        # print 2016 - int(r['BIRTH_YEAR'])
        # print ''
        # if c % 500:
            # print 'its odd'
        print ''
        c += 1
    # print thing
    # print thing_1

# End File: politeauthority/co_voters/parse_voters.py

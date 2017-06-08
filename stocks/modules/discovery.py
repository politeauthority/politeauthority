"""
discovery.py

Usage:
  discovery.py [--do] [options]
  discovery.py  (-h | --help)

Options:
  -h --help             Shows this screen.
  --get_interesting      Fetch Interesting companies only.
  --build_from_nasdaq   Populates company table and last_price column,
                            most likely from the day. Best to run this EOB
  -d --debug            Run the console at debug level



  markets open between 7:30am - 2pm MTN

"""

from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

from modules.company import Company

db = DriverMysql(environmental.mysql_conf())


def emerging_tech_stocks():
    print 'test1'
    qry = """SELECT `id`
             FROM `stocks`.`companies`
             WHERE
                sector="Technology"
                AND
                ipo_year="2017"
            ORDER BY last_sale;
        """
    print qry
    companies = db.ex(qry)
    ret = {}
    for c in companies:
        comp = Company()
        comp.get_company_by_id(c[0])
        ret[comp.symbol] = {'comp': comp}
    return ret

# End File

import sys
import os
import logging

from flask import Flask
from flask import render_template
from flask_debugtoolbar import DebugToolbarExtension

from politeauthority import misc_time

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from modules.company import Company
from modules import company_collections
from modules import quote_collections


def register_logging(app):
    app_log_file = os.path.join(app.config['LOG_DIR'], 'stocky.log')
    logging.basicConfig(filename=app_log_file, level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.TimedRotatingFileHandler(
        app_log_file,
        when='midnight',
        backupCount=20)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


def register_jinja_funcs(app):
    app.jinja_env.filters['time_ago'] = misc_time.ago
    app.jinja_env.filters['fmt_date'] = misc_time.fmt_date


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'KEYKEYKEY'
toolbar = DebugToolbarExtension(app)
register_jinja_funcs(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/company/<symbol>')
def company(symbol):
    company = Company().get_by_symbol(symbol)
    company.load()
    # company.load_quotes()
    d = {
        'company': company,
        'quotes': quote_collections.get_by_company_id(company.id)
    }
    if company:
        company.save_webhit()
        return render_template('company.html', **d)
    else:
        return '404'


@app.route('/recent')
def recent():
    companies = company_collections.get_recently_modified()
    d = {
        'company_count': company_collections.get_count(),
        'companies': companies
    }
    # d['pages'] = round(data['company_count'] / 40, 0)
    return render_template('recent.html', **d)


@app.route('/company_data/<company_id>/quote_data.js')
def company_data(company_id):
    quotes = quote_collections.get_by_company_id(company_id)
    if not quotes:
        return 'ERROR'
    d = {
        'quotes': quotes
    }
    return render_template('morris_quote.js', **d)


# End File stocks/flask/app.py

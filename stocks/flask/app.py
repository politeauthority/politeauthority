import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from datetime import timedelta

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask_debugtoolbar import DebugToolbarExtension

from politeauthority import misc_time
from politeauthority import common

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from modules.company import Company
from modules import portfolio_event_collections
from modules import company_collections
from modules import quote_collections
from helpers import jinja_filters


def register_logging(app):
    app_log_file = os.path.join(app.config['LOG_DIR'], 'stocky.log')
    logging.basicConfig(filename=app_log_file, level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = TimedRotatingFileHandler(
        app_log_file,
        when='midnight',
        backupCount=20)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


def register_jinja_funcs(app):
    app.jinja_env.filters['time_ago'] = misc_time.ago
    app.jinja_env.filters['fmt_date'] = misc_time.fmt_date
    app.jinja_env.filters['fmt_currency'] = jinja_filters.format_currency
    app.jinja_env.filters['percentage'] = common.get_percentage


app = Flask(__name__)
app.config.from_envvar('PA_STOCKS_CONFIG')
toolbar = DebugToolbarExtension(app)
register_jinja_funcs(app)
register_logging(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/company/<symbol>')
def company(symbol):
    company = Company().get_by_symbol(symbol)
    company.load()
    company.avg_52_weeks = quote_collections.get_avg_company_id(company.id)
    d = {
        'company': company,
    }
    if company:
        company.save_webhit()
        return render_template('company.html', **d)
    else:
        return '404'


@app.route('/company_data/<company_id>/quote_data.js')
def company_data(company_id):
    quotes = quote_collections.get_by_company_id(company_id)
    if not quotes:
        return 'ERROR'
    d = {
        'quotes': quotes
    }
    return render_template('json/company_quote.js', **d)


@app.route('/recent')
def recent():
    companies = company_collections.get_recently_modified()
    d = {
        'company_count': company_collections.get_count(),
        'companies': companies
    }
    # d['pages'] = round(data['company_count'] / 40, 0)
    return render_template('recent.html', **d)


@app.route('/watch')
def watch():
    companies = company_collections.get_watch_list()
    d = {
        'companies': companies
    }
    return render_template('recent.html', **d)


@app.route('/portfolio')
def portfolio():
    portfolio = portfolio_event_collections.get_by_portfolio_id(1, True)
    d = {
        'portfolio': portfolio,
        'companies': portfolio['companies'],
        'events': portfolio['events']
    }
    return render_template('portfolio.html', **d)


@app.route('/portfolio_data/<portfolio_id>/quote_data.js')
def portfolio_data(portfolio_id):
    companies = []
    oldest_date = None
    portfolio = portfolio_event_collections.get_by_portfolio_id(portfolio_id)
    for e in portfolio['events']:
        if e.company_id not in companies:
            companies.append(e.company_id)
        if not oldest_date:
            oldest_date = e.date
        if e.date < oldest_date:
            oldest_date = e.date
    one_year_ago = timedelta(days=365)
    if oldest_date > datetime.now() - one_year_ago:
        query_date = oldest_date
    else:
        query_date = datetime.now() - one_year_ago
    quotes = quote_collections.get_by_company_ids(companies, query_date)
    if not quotes:
        return 'ERROR'
    d = {
        'quotes': quotes
    }
    return render_template('json/portfolio_quote.js', **d)
# End File stocks/flask/app.py

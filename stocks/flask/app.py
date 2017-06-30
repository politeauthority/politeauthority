import sys
import os

from flask import Flask
from flask import render_template
from flask_debugtoolbar import DebugToolbarExtension

from politeauthority import misc_time

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from modules.company import Company
from modules import company_collections
from modules import quote_collections


def register_jinja_funcs(app):
    app.jinja_env.filters['time_ago'] = misc_time.ago


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

"""
    Home - CONTROLLER
from flask import Blueprint, request, render_template, flash, g, session, redirect

"""

from flask import Blueprint, render_template

from app.models.company import Company

home = Blueprint('Home', __name__, url_prefix='/')


@home.route('')
def index():
    return render_template('home/index.html')


@home.route('company/<symbol>')
def company(symbol=None):
    company = Company.query.filter(
        Company.symbol == symbol).one()
    d = {}
    d['company'] = company
    return render_template('home/company.html', **d)


@home.route('companies')
def companies():
    c_query = Company.query.order_by(Company.ts_updated)
    d = {}
    d['companies'] = Company.query.order_by(Company.ts_updated).all()
    d['total_companies'] = c_query.count()
    return render_template('home/companies.html', **d)

# End File: app/controllers/home.py

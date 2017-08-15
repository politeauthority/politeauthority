"""App

"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

if os.environ.get('PA_BULD') == 'live':
    app.config.from_pyfile('config/live.py')
else:
    app.config.from_pyfile('config/dev.py')

db = SQLAlchemy(app)

from app.models.company import Company
from app.models.portfolio import Portfolio
from app.models.portfolio_event import PortfolioEvent
from app.models.quote import Quote

from controllers.home import home as ctrl_home
app.register_blueprint(ctrl_home)

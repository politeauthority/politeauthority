"""App

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from politeauthority import environmental

app = Flask(__name__)
mysql_conf = environmental.mysql_conf()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (
    mysql_conf['user'],
    mysql_conf['pass'],
    mysql_conf['host'],
    3306,
    'stocks2')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# from models.company import Company
from controllers.home import home as ctrl_home
app.register_blueprint(ctrl_home)

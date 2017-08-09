"""App

"""

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from politeauthority import environmental

app = Flask(__name__)
db = SQLAlchemy(app)
from models.company import Company

mysql_conf = environmental.mysql_conf()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (
    mysql_conf['user'],
    mysql_conf['pass'],
    mysql_conf['host'],
    3306,
    'stocks2')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def show_all():
	return ''
    # return render_template('show_all.html', students=Company.query.all())

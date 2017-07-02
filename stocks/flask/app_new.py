import logging
import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurations
app.config.from_object('config')

db = SQLAlchemy(app)


def app_logging():
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

   console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(console_handler)

   werkzeug_log = logging.getLogger('werkzeug')
    werkzeug_log.setLevel(logging.DEBUG)
    # werkzeug_log.setFormatter( formatter )
    werkzeug_log.addHandler(file_handler)
    werkzeug_log.addHandler(console_handler)

@app.route('/')
def hello_world():
    return 'Hello, World!'






@app.errorhandler(404)
def not_found(error):
    return redirect('/404')
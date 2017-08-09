"""Install

"""
from app import app
from app import db


if __name__ == '__main__':
    app.logger.info('Runing Installer')
    db.create_all()

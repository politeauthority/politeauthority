"""Company

"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func

from app import db


class Company(db.Model):

    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    ts_created = Column(DateTime, default=func.current_timestamp())
    ts_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    symbol = Column(String(10), nullable=False)
    name = Column(String(128), nullable=False)
    price = Column(Float, nullable=False)
    market_cap = Column(Float, nullable=True)
    ipo_year = Column(String(20), nullable=True)
    sector = Column(String(128), nullable=True)
    industry = Column(String(128), nullable=True)
    exchange = Column(String(128), nullable=True)
    high_52_weeks = Column(Float, nullable=True)
    high_52_weeks_date = Column(DateTime, nullable=True)
    low_52_weeks = Column(Float, nullable=True)
    low_52_weeks_date = Column(DateTime, nullable=True)
    run_company = Column(Integer, nullable=True)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Company %r, %r>' % (self.symbol, self.name)

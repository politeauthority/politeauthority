"""Portfolio

"""
from sqlalchemy import Column, Integer, String, DateTime, func

from app import db


class Portfolio(db.Model):

    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True)
    ts_created = Column(DateTime, default=func.current_timestamp())
    ts_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    user_id = Column(Integer, nullable=False)
    name = Column(String(20), nullable=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Portfolio %r, %r>' % (self.symbol, self.name)

"""Quote

"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func

from app import db


class PortfolioEvent(db.Model):

    __tablename__ = 'portfolio_events'

    id = Column(Integer, primary_key=True)
    ts_created = Column(DateTime, default=func.current_timestamp())
    ts_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    portfolio_id = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    type = Column(String(10), nullable=False)
    date = Column(DateTime, nullable=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<PortfolioEvent %r, %r>' % (self.id, self.name)

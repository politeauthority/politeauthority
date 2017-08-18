"""Quote

"""
from sqlalchemy import Column, Integer, Float, DateTime, func

from app import db


class Quote(db.Model):

    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    ts_created = Column(DateTime, default=func.current_timestamp())
    ts_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    company_id = Column(Integer, nullable=False)
    open = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

    def __init__(self, _id=None):
        if _id:
            self.id = _id

    def __repr__(self):
        return '<Quote %r, %r>' % (self.id, self.name)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

# End File: stocks/app/models/company.py

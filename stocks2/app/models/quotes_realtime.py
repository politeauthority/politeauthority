"""QuoteRealtime

"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func, UniqueConstraint

from app import db


class QuoteRealtime(db.Model):

    __tablename__ = 'quotes_realtime'

    id = Column(Integer, primary_key=True)
    ts_created = Column(DateTime, default=func.current_timestamp())
    ts_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    open = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint('company_id', 'date', name='uix_1'),
    )

    def __init__(self, _id=None):
        if _id:
            self.id = _id

    def __repr__(self):
        return '<QuoteRealtime %r, %r>' % (self.id, self.company_id)

    def save(self):
        exists = None
        if not self.id:
            exists = self.query.filter(
                QuoteRealtime.company_id == self.company_id,
                QuoteRealtime.date == self.date).one_or_none()
        if not self.id and not exists:
            db.session.add(self)
        db.session.commit()

# End File: stocks/app/models/company.py

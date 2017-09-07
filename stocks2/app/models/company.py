"""Company

"""
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from sqlalchemy import PickleType, Text, ForeignKey, func
from sqlalchemy.orm import relationship
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
    meta = relationship('CompanyMeta', back_populates="company")

    __table_args__ = (
        UniqueConstraint('symbol', 'exchange', name='uix_1'),
    )

    def __init__(self, _id=None):
        if _id:
            self.id = _id

    def __repr__(self):
        return '<Company %r, %r>' % (self.symbol, self.name)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()


class CompanyMeta(db.Model):

    __tablename__ = 'companies_meta'

    id = Column(Integer, primary_key=True)
    ts_created = Column(DateTime, default=func.current_timestamp())
    ts_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    key = Column(String(256))
    val_type = Column(String(256))
    val_string = Column(Text())
    val_pickle = Column(PickleType())
    val_date = Column(DateTime)
    company = relationship("Company", back_populates="meta")

    def __repr__(self):
        return '<CompanyMeta %s, %s>' % (self.id, self.value)

# End File: stocks/app/models/company.py

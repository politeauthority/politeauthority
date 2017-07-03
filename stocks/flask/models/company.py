"""
    MODEL Company
"""

import app
print app
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.database import Base


# class TBASE(Model):
#     __abstract__ = True

#     id = Column(Integer,
#                    primary_key=True)
#     ts_created = Column(DateTime,
#                            default=func.current_timestamp())
#     ts_updated = Column(DateTime,
#                            default=func.current_timestamp(),
#                            onupdate=func.current_timestamp())

#     def save(self):
#         if not self.id:
#             new = self
#             session.add(new)
#         session.commit()

#     def delete(self):
#         if self.id:
#             delete_item = self.query.filter(id == self.id)
#             app.logger.debug(delete_item)
#             if not delete_item:
#                 return False
#             session.delete(delete_item)
#             session.commit()
#             return True
#         return False


class Company(Base):

    __tablename__ = 'companies'
    id = Column(Integer,
                primary_key=True)
    ts_created = Column(DateTime,
                        default=func.current_timestamp())
    ts_updated = Column(DateTime,
                        default=func.current_timestamp(),
                        onupdate=func.current_timestamp())
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

    def __init__(self, id=None, symbol=None):
        if id:
            self.id = id
            p = self.query.filter(Company.id == id).first()
            if p:
                self.__build_obj__(p)
        elif symbol:
            self.symbol = symbol
            p = self.query.filter(Company.symbol == symbol).first()
            if p:
                self.__build_obj__(p)

    def __repr__(self):
        return '<Company %r, %r>' % (self.symbol, self.name)

    def __build_obj__(self, c):
        self.id = c.id
        self.symbol = c.symbol
        self.name = c.name
        self.price = c.price
        self.market_cap = c.market_cap
        self.ipo_year = c.ipo_year
        self.sector = c.sector
        self.industry = c.industry
        self.exchange = c.exchange
        self.high_52_weeks = c.high_52_weeks
        self.high_52_weeks_date = c.high_52_weeks_date
        self.low_52_weeks = c.low_52_weeks
        self.low_52_weeks_date = c.low_52_weeks_date
        self.run_company = c.run_company
        self.ts_created = c.ts_created
        self.ts_updated = c.ts_updated

# End File: stocks/models/company.py

"""
    Company Model

    COMPANY TABLE
    CREATE TABLE `stocks`.`companies` (
      `id`                  BIGINT(20) unsigned NOT NULL AUTO_INCREMENT,
      `symbol`              VARCHAR(10) DEFAULT NULL,
      `name`                VARCHAR(255) DEFAULT NULL,
      `price`               DECIMAL(20,4) DEFAULT NULL,
      `market_cap`          DECIMAL(20,4) DEFAULT NULL,
      `ipo_year`            VARCHAR(10) DEFAULT NULL,
      `sector`              VARCHAR(255) DEFAULT NULL,
      `industry`            VARCHAR(255) DEFAULT NULL,
      `exchange`            VARCHAR(50) DEFAULT NULL,
      `high_52_weeks`       DECIMAL(20,4) DEFAULT NULL,
      `high_52_weeks_date`  DATETIME DEFAULT NULL,
      `low_52_weeks`        DECIMAL(20,4) DEFAULT NULL,
      `low_52_weeks_date`   DATETIME DEFAULT NULL,
      `run_company`         TINYINT(1) DEFAULT NULL,
      `ts_created`          DATETIME DEFAULT CURRENT_TIMESTAMP,
      `ts_updated`          DATETIME ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`),
      KEY `symbol` (`symbol`),
      UNIQUE KEY `unique_index` (`symbol`, `exchange`)
    );

"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, func

Base = declarative_base()


class BaseModel(Base):
    id = Column(Integer, primary_key=True)
    ts_created = Column(DateTime,
                        default=func.current_timestamp())
    ts_updated = Column(DateTime,
                        default=func.current_timestamp(),
                        onupdate=func.current_timestamp())


class Company(BaseModel):
    __tablename__ = 'companies'

    symbol = Column(String(6), key=True)
    name = Column(String(250))
    price = Column(Float)
    market_cap = Column(Float)
    ipo_year = Column(String(4))
    sector = Column(String(50))
    industry = Column(String(50))
    exchange = Column(String(20))
    high_52_weeks = Column(Float)
    high_52_weeks_date = Column(DateTime)
    low_52_weeks = Column(Float)
    low_52_weeks_date = Column(DateTime)

    def __repr__(self):
        return '<Company %r, %r>' % (self.symbol, self.name)

# End File: stocks/modules/company.py

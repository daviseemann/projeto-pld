from typing import Optional
from sqlalchemy import Column, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Definição da tabela PLDData
class PLDData(Base):
    __tablename__ = "pld_data"
    id = Column(String, primary_key=True, index=True)
    submarket = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime)

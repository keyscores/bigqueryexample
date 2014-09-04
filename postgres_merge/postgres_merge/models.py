from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import HSTORE

Base = declarative_base()


class RawData(Base):
    __tablename__ = 'raw_data'

    id = Column(Integer, primary_key=True)
    data = Column(MutableDict.as_mutable(HSTORE))
    connector = Column(String, nullable=False)
    version = Column(Integer, nullable=False, default=0)
    sheet_name = Column(String, nullable=False)
    file_name = Column(String, nullable=False)


class MergedData(Base):
    __tablename__ = 'merged_data'

    id = Column(Integer, primary_key=True)
    data = Column(MutableDict.as_mutable(HSTORE))
    connector = Column(String, nullable=False)
    version = Column(Integer, nullable=False, default=0)

from typing import Any

from sqlalchemy import BOOLEAN, TIMESTAMP, Column, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import FLOAT, TIMESTAMP, Integer

Base: Any = declarative_base()


class TestResult(Base):
    __tablename__ = "test_result"
    id = Column(Integer, primary_key=True)
    class_name = Column(Text, nullable=False)
    test_name = Column(Text, nullable=False)
    passed = Column(BOOLEAN, nullable=False)
    message = Column(Text, nullable=True)
    timestamp = Column(TIMESTAMP, nullable=False)
    duration_millis = Column(FLOAT, nullable=False)
    repo = Column(Text, nullable=False)
    branch = Column(Text, nullable=False)
    sha = Column(Text, nullable=False)

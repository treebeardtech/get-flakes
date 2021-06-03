from typing import Any

from sqlalchemy import BOOLEAN, TIMESTAMP, Column, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import FLOAT, TIMESTAMP, Integer

Base: Any = declarative_base()

engine = create_engine(
    # local dev credentials
    "cockroachdb://panoptes:panoptes@localhost:26257/panoptes?sslmode=require",
    echo=False,  # Log SQL queries to stdout
)
Session = sessionmaker(engine)


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


if __name__ == "__main__":
    Base.metadata.create_all(engine)

from sqlalchemy import create_engine, Column, BOOLEAN, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP

Base = declarative_base()

engine = create_engine(
    # local dev credentials
    'cockroachdb://panoptes:panoptes@localhost:26257/panoptes?sslmode=require',
    echo=True                   # Log SQL queries to stdout
)

class TestResult(Base):
    """The Account class corresponds to the "accounts" database table.
    """
    __tablename__ = 'test_result'
    id = Column(UUID(as_uuid=True), primary_key=True)
    class_name = Column(Text, nullable=False)
    test_name = Column(Text, nullable=False)
    passed = Column(BOOLEAN, nullable=False)
    message = Column(Text, nullable=True)
    timestamp = Column(TIMESTAMP, nullable=False)
    repo = Column(Text, nullable=False)
    branch = Column(Text, nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
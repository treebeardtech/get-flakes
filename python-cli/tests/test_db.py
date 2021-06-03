import os.path
from pathlib import Path

import pytest
from deeptest.backend.models import Base
from deeptest.db import Db
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker


@pytest.fixture
def session():
    engine = create_engine("sqlite://", echo=False)
    Base.metadata.create_all(engine)
    return sessionmaker(engine)()


def test_store(session):
    db = Db(session)
    test_path = Path(os.path.join(os.path.dirname(__file__), "report.xml"))
    db.store(test_path, "feature/test", "test-repo", "A_SHA")


def test_check(session):
    db = Db(session)
    test_path = Path(os.path.join(os.path.dirname(__file__), "report.xml"))
    db.store(test_path, "feature/test", "test-repo", "A_SHA")
    db.store(test_path, "feature/test2", "test-repo", "A_SHA")

    flakes = db.check_store(test_path, "feature/test3", "test-repo", "A_SHA")
    assert len(flakes) == 2

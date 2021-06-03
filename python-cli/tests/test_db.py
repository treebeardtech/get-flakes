import datetime
import os.path
from pathlib import Path

import pytest
from deeptest.backend.models import Base
from deeptest.db import Db, FlakyTest, FlakyTestRun
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


def test_get_flakes(session):
    db = Db(session)
    test_path = Path(os.path.join(os.path.dirname(__file__), "report.xml"))
    db.store(test_path, "feature/test", "test-repo", "sha1")
    test_path = Path(os.path.join(os.path.dirname(__file__), "report_passed.xml"))
    db.store(test_path, "feature/test", "test-repo", "sha1")

    flakes = db.get_flakes("test-repo")
    assert flakes[0] == FlakyTest(
        class_name="tests.test_flakiness_simulator",
        test_name="test_eval[23]",
        runs=[
            FlakyTestRun(
                sha="sha1", date=datetime.datetime(2021, 6, 3, 12, 35, 2, 780482)
            )
        ],
    )
    assert flakes[1] == FlakyTest(
        class_name="tests.test_flakiness_simulator",
        test_name="test_eval[88]",
        runs=[
            FlakyTestRun(
                sha="sha1", date=datetime.datetime(2021, 6, 3, 12, 35, 2, 780482)
            )
        ],
    )

def test_get_flakes_with_date(session):
    db = Db(session)
    test_path = Path(os.path.join(os.path.dirname(__file__), "report.xml"))
    db.store(test_path, "feature/test", "test-repo", "sha1")
    test_path = Path(os.path.join(os.path.dirname(__file__), "report_passed.xml"))
    db.store(test_path, "feature/test", "test-repo", "sha1")

    flakes = db.get_flakes("test-repo", datetime.datetime.now())
    assert flakes == []
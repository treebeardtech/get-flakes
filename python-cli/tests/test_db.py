import os.path
from pathlib import Path

from deeptest.db import Db


def test_store():
    db = Db()
    test_path = Path(os.path.join(os.path.dirname(__file__), "report.xml"))
    db.store(test_path, "feature/test", "test-repo", "A_SHA")


def test_check():
    db = Db()
    test_path = Path(os.path.join(os.path.dirname(__file__), "report.xml"))
    db.store(test_path, "feature/test", "test-repo", "A_SHA")
    db.store(test_path, "feature/test2", "test-repo", "A_SHA")

    flakes = db.check_store(test_path, "feature/test3", "test-repo", "A_SHA")
    print(flakes)

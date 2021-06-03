import os.path
from deeptest.backend.models import Session, TestResult
from deeptest.db import Db

def test_store():
    db = Db()
    test_path = os.path.join(os.path.dirname(__file__), "report.xml")
    db.store(test_path, "feature/test", "test-repo", "A_SHA")

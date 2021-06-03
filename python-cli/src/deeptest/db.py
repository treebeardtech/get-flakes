from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from deeptest.backend.models import TestResult
from junitparser import JUnitXml
from junitparser.junitparser import TestCase
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker


@dataclass
class Failure:
    date: datetime
    duration_millis: float
    stderr: str
    stdout: Optional[str]


@dataclass
class FailingTest:
    failures: List[Failure]


@dataclass
class TestRun:
    sha: str
    date: datetime


@dataclass
class FlakyTest:
    runs: List[TestRun]


DATABASE_URL = "sqlite://"
# DATABASE_URL = cockroachdb://panoptes:panoptes@localhost:26257/panoptes?sslmode=require",

engine = create_engine(
    # local dev credentials
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,  # Log SQL queries to stdout
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionLocal()
    try:
        yield Db(session)
    finally:
        session.close()


class Db:
    def __init__(self, session) -> None:
        self.session = session

    def store(self, junit_xml_path: Path, branch: str, repo: str, sha: str):
        xml = JUnitXml.fromfile(junit_xml_path)

        for suite in xml:
            if suite is None:
                continue

            for testcase in suite:
                test_result = TestResult(
                    class_name=testcase.classname,
                    test_name=testcase.name,
                    passed=len(testcase.result) == 0,
                    message="\n".join(result.text for result in testcase.result),
                    duration_millis=testcase.time,
                    branch=branch,
                    repo=repo,
                    sha=sha,
                    timestamp=datetime.fromisoformat(suite.timestamp),
                )
                self.session.add(test_result)
        self.session.commit()

    def get_flakes(self, repo: str, since_date: datetime) -> List[FlakyTest]:
        return []

    def check_store(
        self, junit_xml_path: Path, branch: str, repo: str, sha: str
    ) -> List[FailingTest]:
        xml = JUnitXml.fromfile(junit_xml_path)

        failures: List[TestCase] = []
        for suite in xml:
            if suite is None:
                continue
            for testcase in suite:
                if len(testcase.result) > 0:
                    failures.append(testcase)

        flakes = []
        for failure in failures:
            previous_failures = (
                self.session.query(TestResult)
                .filter(TestResult.test_name == failure.name)
                .filter(TestResult.class_name == failure.classname)
                .filter(TestResult.repo == repo)
                .filter(TestResult.passed == False)
                .limit(100)
                .all()
            )

            distinct_branches = set([result.branch for result in previous_failures])

            if len(distinct_branches) >= 2 and len(previous_failures) >= 2:
                failures = [
                    Failure(
                        date=result.timestamp,
                        duration_millis=result.duration_millis,
                        stderr=result.message,
                        stdout=None,
                    )
                    for result in previous_failures
                ]
                flakes.append(FailingTest(failures=failures))

        return flakes

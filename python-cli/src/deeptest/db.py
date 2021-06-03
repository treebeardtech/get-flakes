from datetime import datetime
from pathlib import Path
from typing import Dict, List
from deeptest.backend.models import Session, TestResult
from junitparser import JUnitXml


class Failure:
    date: datetime
    duration_millis: float
    stderr: str
    stdout: str


class FlakyTest:
    failures: List[Failure]


class Db:
    def __init__(self) -> None:
        pass

    def store(self, junit_xml_path: Path, branch: str, repo: str, sha: str):
        xml = JUnitXml.fromfile(junit_xml_path)

        with Session() as session:
            for suite in xml:
                if suite is None:
                    continue
                # handle suites
                for testcase in suite:
                    key: str = f"{testcase.classname}.{testcase.name}"
                    test_result = TestResult(
                        class_name=testcase.classname,
                        test_name=testcase.name,
                        passed=len(testcase.result) == 0,
                        message="\n".join(result.text for result in testcase.result),
                        duration_millis=testcase.time,
                        branch=branch,
                        repo=repo,
                        sha=sha,
                        timestamp=suite.timestamp
                    )
                    session.add(test_result)
            session.commit()

    def check_store(
        self, junit_xml_path: Path, branch: str, repo: str, sha: str
    ) -> List[FlakyTest]:
        return []

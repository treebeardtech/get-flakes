from datetime import datetime
from pathlib import Path
from typing import List


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
        pass

    def check_store(
        self, junit_xml_path: Path, branch: str, repo: str, sha: str
    ) -> List[FlakyTest]:
        return []

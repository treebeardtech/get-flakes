from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class CheckConclusionState(str, Enum):
    ACTION_REQUIRED = "ACTION_REQUIRED"
    TIMED_OUT = "TIMED_OUT"
    CANCELLED = "CANCELLED"
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"
    NEUTRAL = "NEUTRAL"
    SKIPPED = "SKIPPED"
    STARTUP_FAILURE = "STARTUP_FAILURE"
    STALE = "STALE"


class App(BaseModel):
    name: str


class CheckRun(BaseModel):
    databaseId: str
    conclusion: Optional[CheckConclusionState]
    name: str


class CheckRuns(BaseModel):
    nodes: List[CheckRun]


class CheckSuite(BaseModel):
    app: App
    checkRuns: CheckRuns


class CheckSuites(BaseModel):
    nodes: List[CheckSuite]


class Commit(BaseModel):
    oid: str
    checkSuites: CheckSuites


class Commits(BaseModel):
    commit: List[Commit]


class PRCommit(BaseModel):
    commit: Commit


class PRCommits(BaseModel):
    nodes: List[PRCommit]


class PullRequest(BaseModel):
    number: int
    commits: PRCommits

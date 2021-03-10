import json
from enum import Enum
from itertools import groupby
from pathlib import Path
from typing import Dict, List, cast

import click
from coverage import CoverageData
from junitparser import JUnitXml
from pydantic import BaseModel


class Line(BaseModel):
    passed: List[str]
    failed: List[str]


class File(BaseModel):
    lines: Dict[int, Line]


class Status(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


def _get_line(contexts: List[str], status: Dict[str, Status]):
    def _get_status(test_case: str):
        key = test_case.split("|")[0].replace(".py::", ".").replace("/", ".")
        return status.get(key)

    line_data = {k: list(g) for k, g in groupby(contexts, _get_status)}

    return Line(
        passed=line_data.get(Status.SUCCESS, []),
        failed=line_data.get(Status.FAILURE, []),
    )


@click.command()
@click.argument("source")
def run(source: str):
    """"""
    xml = JUnitXml.fromfile("junit.xml")

    status: Dict[str, Status] = {}
    for suite in xml:
        if suite is None:
            continue
        # handle suites
        for testcase in suite:
            key: str = f"{testcase.classname}::{testcase.name}"
            status[key] = (
                Status.SUCCESS if len(testcase.result) == 0 else Status.FAILURE
            )

    cd = CoverageData()
    cd.read()
    cl = cast(Dict[int, List[str]], cd.contexts_by_lineno(Path(source).as_posix()))
    cl
    file = File(lines={i: _get_line(cl[i], status) for i in cl.keys()})
    output = json.dumps(file.dict())
    click.echo(output)

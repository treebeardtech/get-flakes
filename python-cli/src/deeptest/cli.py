import json
from enum import Enum
from pathlib import Path
from typing import Dict, List, cast

import click
from coverage import Coverage, CoverageData
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


class ContextStatus(BaseModel):
    ctx: str
    status: Status


def norm(context: str):
    return (
        context.split("|")[0].replace(".py::", ".").replace("/", ".").replace("::", ".")
    )


def _get_line(contexts: List[str], status: Dict[str, Status]):
    if contexts == [""]:
        return Line(passed=["ran on startup"], failed=[])

    context_statuses = list(
        map(lambda ctx: ContextStatus(ctx=ctx, status=status[ctx]), contexts)
    )

    return Line(
        passed=[ctxs.ctx for ctxs in context_statuses if ctxs.status == Status.SUCCESS],
        failed=[ctxs.ctx for ctxs in context_statuses if ctxs.status == Status.FAILURE],
    )


@click.command()
@click.argument("source")
def run(source: str):
    """"""
    src = Path(source).as_posix()
    xml = JUnitXml.fromfile("junit.xml")

    status: Dict[str, Status] = {"": Status.SUCCESS}
    for suite in xml:
        if suite is None:
            continue
        # handle suites
        for testcase in suite:
            key: str = f"{testcase.classname}.{testcase.name}"
            status[key] = (
                Status.SUCCESS if len(testcase.result) == 0 else Status.FAILURE
            )
    c = Coverage()
    c.load()
    cd = CoverageData()
    cd.read()
    missing_lines = {num: Line(passed=[], failed=[]) for num in c.analysis2(src)[3]}
    norm_contexts = {norm(ctx) for ctx in cd.measured_contexts()}
    assert norm_contexts.difference(status.keys()) == set()

    cl = cast(Dict[int, List[str]], cd.contexts_by_lineno(src))
    cl = {ln: list(map(norm, cl[ln])) for ln in cl.keys()}

    file = File(
        lines={**missing_lines, **{i: _get_line(cl[i], status) for i in cl.keys()}}
    )
    output = json.dumps(file.dict())
    click.echo(output)


# src/test_lib.py::test_divide2[3.0]|run == src.test_lib::test_divide2[3.0]

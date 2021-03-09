import json
from typing import Dict, List

import click
from coverage import CoverageData
from pydantic import BaseModel
from rich.console import Console
from rich.syntax import Syntax


class Line(BaseModel):
    passed: List[str]
    failed: List[str]


class File(BaseModel):
    lines: List[Line]


@click.command()
def run():
    """"""
    cd = CoverageData()
    cd.read()
    cl: Dict[int, List[str]] = cd.contexts_by_lineno(
        "/Users/a/git/treebeardtech/deeptest/debug/src/bl/test_main.py"
    )
    cl
    file = File(lines=[Line(passed=["adf"], failed=["kjh"])])
    syntax = Syntax(json.dumps(file.dict()), "json")
    console = Console()
    console.print(syntax)

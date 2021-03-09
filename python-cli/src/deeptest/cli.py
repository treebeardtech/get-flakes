import json
from typing import List

import click
from pydantic import BaseModel


class Line(BaseModel):
    passed: List[str]
    failed: List[str]


class File(BaseModel):
    lines: List[Line]


@click.command()
def run():
    """"""
    from rich.console import Console
    from rich.syntax import Syntax

    file = File(lines=[Line(passed=["adf"], failed=["kjh"])])
    syntax = Syntax(json.dumps(file.dict()), "json")
    console = Console()
    console.print(syntax)

import json
import os

from click.testing import CliRunner

from deeptest import cli

pytest_plugins = "pytester"
from pathlib import Path

RESOURCES = (Path(__file__) / ".." / "resources").resolve()


def setup():
    os.chdir(RESOURCES)


def test_when_local_dir_then_success():
    runner = CliRunner()
    result = runner.invoke(cli.run, catch_exceptions=False)

    f = cli.File(**json.loads(result.stdout))
    f

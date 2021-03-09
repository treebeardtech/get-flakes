import json
import os

from click.testing import CliRunner

from deeptest import cli

pytest_plugins = "pytester"
from pathlib import Path

RESOURCES = (Path(__file__) / ".." / "resources").resolve()


def setup():
    os.chdir(RESOURCES / ".deeptest")


def test_when_local_dir_then_success():
    runner = CliRunner()
    source = (RESOURCES / "src" / "test_main.py").as_posix()
    print(f"Running {source}")
    result = runner.invoke(cli.run, source, catch_exceptions=False)

    print(result.stdout)
    f = cli.File(**json.loads(result.stdout))
    assert f.lines[9].passed == ["src.test_main::test_add"]
    assert f.lines[4].passed == []
    assert f.lines[4].failed == []
    assert f.lines[5].passed == [
        "src.test_main::test_add",
        "src.test_main::test_add2[3.0]",
    ]
    assert f.lines[5].failed == ["src.test_main::test_add2[0]"]

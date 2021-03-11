import json
import os

from click.testing import CliRunner
from deeptest.cli import File, Line

from deeptest import cli

pytest_plugins = "pytester"
import sys
from pathlib import Path
from subprocess import CalledProcessError, check_output

RESOURCES = (Path(__file__) / ".." / "resources").resolve()


def setup_module():
    check_output("rm -rf deeptest", shell=True)
    try:
        check_output(f"{sys.executable} -m pytest", cwd="tests/resources", shell=True)
    except CalledProcessError as err:
        assert err.returncode == 1


def setup():
    os.chdir(RESOURCES / ".deeptest")


def test_when_local_dir_then_success():
    runner = CliRunner()
    source = RESOURCES / "src" / "test_lib.py"
    assert source.exists()
    print(f"Running {source}")
    result = runner.invoke(cli.run, source.as_posix(), catch_exceptions=False)

    print(result.stdout)
    f = File(**json.loads(result.stdout))
    assert f.lines[7].passed == ["src/test_lib.py::test_divide|run"]
    assert f.lines[3] == Line(passed=[], failed=[])
    assert f.lines[12] == Line(
        passed=[
            "src/test_lib.py::test_divide2[3.0]|run",
        ],
        failed=["src/test_lib.py::test_divide2[0]|run"],
    )
    assert f.lines[17] == Line(
        passed=["src/test_lib.py::TestLib::test_hello|run"], failed=[]
    )
    assert f.lines[21] == Line(
        passed=["src/test_lib.py::TestLib::test_divide2[3.0]|run"],
        failed=["src/test_lib.py::TestLib::test_divide2[0]|run"],
    )


def test_when_local_dir_then_success():
    runner = CliRunner()
    source = RESOURCES / "src" / "lib.py"
    assert source.exists()
    print(f"Running {source}")
    result = runner.invoke(cli.run, source.as_posix(), catch_exceptions=False)

    print(result.stdout)
    f = File(**json.loads(result.stdout))
    expected = """
    {"lines": {"3": {"passed": [], "failed": []}, "1": {"passed": ["ran on startup"], "failed": []}, "2": {"passed": ["src.test_lib.test_divide", "src.test_lib.test_divide2[3.0]", "src.test_lib.TestLib.test_divide2[3.0]"], "failed": ["src.test_lib.test_divide2[0]", "src.test_lib.TestLib.test_divide2[0]"]}, "5": {"passed": ["src.test_lib.test_divide", "src.test_lib.test_divide2[3.0]", "src.test_lib.TestLib.test_divide2[3.0]"], "failed": ["src.test_lib.test_divide2[0]", "src.test_lib.TestLib.test_divide2[0]"]}}}
"""
    assert f == File(**json.loads(expected))

from pathlib import Path

from click.testing import CliRunner
from deeptest import cli

pytest_plugins = "pytester"


class TestCli:
    def test_a(self, testdir):
        Path("junit.xml").write_text("lkj")
        runner = CliRunner()
        result = runner.invoke(cli.run, f"junit.xml", catch_exceptions=False)
        print(result.output)

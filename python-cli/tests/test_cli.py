from click.testing import CliRunner
from get_flakes import cli

pytest_plugins = "pytester"


class TestCli:
    def test_report(self, testdir):
        runner = CliRunner()
        result = runner.invoke(cli.run, f"--days=7", catch_exceptions=False)
        assert result.output.startswith("stub")

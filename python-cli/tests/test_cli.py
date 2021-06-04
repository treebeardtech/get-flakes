import os.path

from click.testing import CliRunner
from get-flakes import cli

pytest_plugins = "pytester"


class TestCli:
    def test_upload(self, testdir):
        runner = CliRunner()
        junit_xml = os.path.join(os.path.dirname(__file__), "report.xml")
        result = runner.invoke(cli.run, f"upload {junit_xml}", catch_exceptions=False)
        print(result.output)

    def test_report(self, testdir):
        runner = CliRunner()
        result = runner.invoke(cli.run, f"report 9", catch_exceptions=False)
        print(result.output)

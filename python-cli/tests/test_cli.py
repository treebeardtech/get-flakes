import os.path

from click.testing import CliRunner
from deeptest import cli

pytest_plugins = "pytester"


class TestCli:
    def test_a(self, testdir):
        runner = CliRunner()
        junit_xml = os.path.join(os.path.dirname(__file__), "report.xml")
        result = runner.invoke(cli.run, junit_xml, catch_exceptions=False)
        print(result.output)

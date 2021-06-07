from click.testing import CliRunner

from get_flakes import cli

pytest_plugins = "pytester"


class TestCli:
    def test_report(self, testdir):
        runner = CliRunner()
        result = runner.invoke(cli.run, f"--days=7", catch_exceptions=False)
        assert isinstance(result, str)

    def test_create_check_run(self):
        cli.create_check_run()

    def test_render_report(self):
        report = cli.render_report(cli.FlakeReport(flake_incidents=[]))
        assert isinstance(report, str)

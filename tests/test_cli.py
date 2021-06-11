from pathlib import Path

from click.testing import CliRunner

from get_flakes import cli
from get_flakes.github import PullRequest

pytest_plugins = "pytester"


class TestCli:
    def test_report(self, testdir):
        runner = CliRunner()
        _ = runner.invoke(cli.run, f"--days=7", catch_exceptions=False)

    def test_create_check_run(self):
        cli.create_check_run((Path(__file__).parent / "example_report.md").read_text())

    def test_render_report(self):
        report = cli.render_report([])
        assert isinstance(report, str)

    def test_fetch(self):
        response = (Path(__file__).parent / "github_response.json").read_text()
        import json

        dd = json.loads(response)["data"]["repository"]["pullRequests"]["nodes"]
        prs = [PullRequest(**pr) for pr in dd]

        fprs = cli.Reporter().get_flaky_prs(prs)
        assert len(fprs) == 1

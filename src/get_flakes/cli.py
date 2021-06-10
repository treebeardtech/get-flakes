import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, DefaultDict, Dict, List, Set

import click
import dotenv
import requests
from click.core import Context
from jinja2 import Environment, select_autoescape
from jinja2.loaders import DictLoader
from pydantic.main import BaseModel
from requests.models import Response

from get_flakes.github import CheckSuite, PullRequest

ENDPOINT = "https://api.github.com/graphql"
TEMPLATE_PATH = Path(__file__).parent / "templates" / "report.html.jinja"
QUERIES_DIR = Path(__file__).parent / "queries"

dotenv.load_dotenv()
token = os.environ["GITHUB_TOKEN"]


class FlakyRun(BaseModel):
    conclusion: str
    url: str


class FlakyCheck(BaseModel):
    name: str
    runs: List[FlakyRun]


class FlakyCommit(BaseModel):
    checks: List[FlakyCheck]
    sha: str
    message: str


class FlakyPR(BaseModel):
    commits: List[FlakyCommit]
    number: int


@dataclass
class FlakeReport:
    flake_incidents: List[PullRequest]


def create_check_run(report_body: str):
    query = (QUERIES_DIR / "create_check_run.graphql").read_text()
    data = {
        "query": query,
        "variables": {
            "sha": "4ee9649155afeeca72f8009c0b86900df170f1ea",
            "text": report_body,
        },
    }
    headers = {"Authorization": f"Bearer {token}"}

    resp: Response = requests.post(ENDPOINT, json=data, headers=headers)
    print(resp.content)
    assert resp.status_code == 200
    output = resp.json()
    if "errors" in output:
        click.echo(json.dumps(output))
        raise RuntimeError(f"Failed to create checkrun {output}")

    return output


def get_api_response(token: str, repo: str, days: int) -> Dict[str, Any]:
    query = (QUERIES_DIR / "get_check_runs.graphql").read_text()
    data = {"query": query}
    headers = {"Authorization": f"Bearer {token}"}

    resp: Response = requests.post(ENDPOINT, json=data, headers=headers)
    assert resp.status_code == 200
    return resp.json()


class Reporter:
    def get_flaky_check(self, name: str, suite: CheckSuite):
        runs: List[FlakyRun] = []
        for run in suite.checkRuns.nodes:
            if run.name == name:
                runs.append(FlakyRun(conclusion=run.conclusion, url="lkj"))
        return FlakyCheck(name=name, runs=runs)

    def get_flaky_prs(self, prs: List[PullRequest]):
        flaky_prs: List[FlakyPR] = []

        for pr in prs:
            flaky_commits: List[FlakyCommit] = []

            for cc in pr.commits.nodes:
                flaky_checks: List[FlakyCheck] = []

                for suite in cc.commit.checkSuites.nodes:
                    conclusions_lookup: Dict[str, Set[str]] = DefaultDict(set)

                    for run in suite.checkRuns.nodes:
                        conclusions_lookup[run.name].add(run.conclusion)

                    for check_run_name, conclusions in conclusions_lookup.items():
                        is_flaky = len(conclusions) > 1

                        if is_flaky:
                            flaky_checks.append(
                                self.get_flaky_check(check_run_name, suite)
                            )

                if len(flaky_checks) > 0:
                    flaky_commit = FlakyCommit(
                        checks=flaky_checks, sha="98", message="lkj"
                    )
                    flaky_commits.append(flaky_commit)

            if len(flaky_commits) > 0:
                flaky_pr = FlakyPR(commits=flaky_commits, number=4)
                flaky_prs.append(flaky_pr)

        return flaky_prs


def render_report(flaky_prs: List[FlakyPR]) -> str:
    env = Environment(
        loader=DictLoader({"report": (TEMPLATE_PATH).read_text()}),
        autoescape=select_autoescape(),
    )
    template = env.get_template("report")
    return template.render(days=9)


@click.command()
@click.option("--debug/--no-debug", default=False)
@click.option("--days", default=7)
@click.pass_context
def run(ctx: Context, debug: bool, days: int):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug

    repo = "treebeardtech/get-flakes"

    api_response: Dict[str, Any] = get_api_response(token, repo, days)
    raw_prs = api_response["data"]["repository"]["pullRequests"]["nodes"]
    prs = [PullRequest(**pr) for pr in raw_prs]
    prs: List[PullRequest] = []
    flaky_prs: List[FlakyPR] = Reporter().get_flaky_prs(prs)
    output: str = render_report(flaky_prs)
    click.echo(output)

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, DefaultDict, Dict, List, OrderedDict, Set

import click
import dotenv
from pydantic.main import BaseModel
import requests
from click.core import Context
from jinja2 import Environment, select_autoescape
from jinja2.loaders import DictLoader
from requests.models import Response

from get_flakes.github import CheckRun, CheckSuite, Commit, PullRequest

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


def get_check_runs(data: Dict[str, Any]):
    # url = f"https://github.com/{repo}/pull/{pr_number}/checks?check_run_id={check_run_id}"
    return []


def get_flake_incidents(check_runs: List[PullRequest]):
    return []

class Reporter:
    flakes = Set()
    cache: Dict[str, Set[CheckRun]] = DefaultDict(Set)

    def create_lookup(self, prs: List[PullRequest]):
        for pr in prs:
            for cc in pr.commits.nodes:
                for suite in cc.checkSuites.nodes:
                    for run in suite.checkRuns.nodes:
                        key = f"{pr.number}_{cc.oid}_{suite.app.name}_{run.name}"
                        if self.cache[key] != Set():
                            self.flakes.add(f"{pr.number}")
                            self.flakes.add(f"{pr.number}_{cc.oid}")
                            self.flakes.add(f"{pr.number}_{cc.oid}_{suite.app.name}")
                            self.flakes.add(key)

                        self.cache[key].add(run)


# for suite in cc.checkSuites.nodes:
#                 frun: List[FlakyRun] = []
#                 for run in suite.checkRuns.nodes:
#                     key = f"{pr.number}_{cc.oid}_{suite.app.name}_{run.name}"
#                     if not key in flakes:
#                         continue

#                     run = FlakyRun()
#                     frun.append(run)
#                 fs = FlakyCheck(name=suite.app.n)
#                 fchecks.append(fs)
    def get_flaky_checks(self, check_suites: List[CheckSuite]) -> List[FlakyCheck]:
        check_lookup: OrderedDict[str, FlakyCheck] = OrderedDict()
        for suite in check_suites:
            for run in suite.checkRuns.nodes:
                key = ".."
                if 
        return list(check_lookup.values())

    def get_flaky_commit(self, commit: Commit) -> FlakyCommit:
        fchecks:List[FlakyCheck] = self.get_flaky_checks(commit.checkSuites.nodes)
        return FlakyCommit(checks=fchecks)

    def get_flaky_prs(self, prs: List[PullRequest]) -> List[FlakyPR]:
        flaky_prs: List[FlakyPR] = []
        for pr in prs:
            if not f"{pr.number}" in self.flakes:
                fccs: List[FlakyCommit] = [self.get_flaky_commit(cc) for cc in pr.commits.nodes if f"{pr.number}_{cc.oid}" in self.flakes]
                fpr = FlakyPR(commits=fccs)
                flaky_prs.append(fpr)
        return flaky_prs


def render_report(flaky_prs: List[PullRequest]) -> str:
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
    prs: List[PullRequest] = get_check_runs(api_response)
    flaky_prs: List[PullRequest] = get_flaky_prs(prs)
    output: str = render_report(flaky_prs)
    click.echo(output)

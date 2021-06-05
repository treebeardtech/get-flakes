import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import click
import dotenv
import requests
from click.core import Context
from requests.models import Response

ENDPOINT = "https://api.github.com/graphql"


@dataclass
class CheckRun:
    repo: str
    sha: str
    pr_number: str
    check_run_id: str
    app: str
    check_name: str
    conclusion: str


@dataclass
class FlakeIncident:
    check_runs: List[CheckRun]


@dataclass
class FlakeReport:
    flake_incidents: List[FlakeIncident]


def get_api_response(token: str, repo: str, days: int) -> Dict[str, Any]:
    query = (Path(__file__).parent / "check_run_query.graphql").read_text()
    data = {"query": query}
    headers = {"Authorization": f"Bearer {token}"}

    resp: Response = requests.post(ENDPOINT, json=data, headers=headers)
    assert resp.status_code == 200
    return resp.json()

def get_check_runs(data: Dict[str, Any]):
    # url = f"https://github.com/{repo}/pull/{pr_number}/checks?check_run_id={check_run_id}"
    return []


def get_flake_incidents(check_runs: List[CheckRun]):
    return []


def get_flake_report(flake_incidents: List[FlakeIncident]):
    return FlakeReport(flake_incidents=[])


def render_report(report: FlakeReport):
    return "stub"


@click.command()
@click.option("--debug/--no-debug", default=False)
@click.option("--days", default=7)
@click.pass_context
def run(ctx: Context, debug: bool, days: int):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug

    dotenv.load_dotenv()
    token = os.environ["GITHUB_TOKEN"]
    repo = "treebeardtech/get-flakes"

    api_response: Dict[str, Any] = get_api_response(token, repo, days)
    check_runs: List[CheckRun] = get_check_runs(api_response)
    flake_incidents: List[FlakeIncident] = get_flake_incidents(check_runs)
    flake_report: FlakeReport = get_flake_report(flake_incidents)
    output: str = render_report(flake_report)
    click.echo(output)

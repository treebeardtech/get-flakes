import click
import requests
from click.core import Context


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.option("--server", default="http://localhost:8080")
@click.pass_context
def run(ctx, debug: bool, server: str):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj["DEBUG"] = debug
    ctx.obj["SERVER"] = server


@run.command()
@click.pass_context
@click.argument("junit_path")
def upload(ctx: Context, junit_path: str):
    with open(junit_path, "rb") as fp:
        files = {"file": fp.read()}
        r = requests.post(f"{ctx.obj['SERVER']}/upload/", files=files)
        assert r.status_code == 200


@run.command()
@click.pass_context
@click.argument("days", default=7)
def report(ctx: Context, days: int):
    r = requests.get(f"{ctx.obj['SERVER']}/report/", params={"days": days})
    assert r.status_code == 200

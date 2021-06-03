import click
import requests


@click.command()
@click.argument("junit_path")
@click.option("--store", default=False)
@click.option("--server", default="http://localhost:8080")
def run(junit_path: str, store: bool, server: str):
    with open(junit_path, "rb") as fp:
        files = {"file": fp.read()}
        # r = requests.get(f"{server}/")
        r = requests.post(f"{server}/upload/", files=files)
        assert r.status_code == 200

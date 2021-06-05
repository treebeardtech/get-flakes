# get-flakes 🍦

**under construction, do not attempt to use.**

**A CI tool that alerts teams when flaky tests are slowing down development**

---

get-flakes notifies you when unreliable tests are hurting your team's productivity so you can prioritise a fix.

Excessive test retrying slows delivery, wastes resources, and hides real bugs.

## Quickstart

Ensure you have Python 3 setup before you start

Install the Python package

```none
pip install get-flakes
```

```log
get-flakes report --days=9
```

| Pull Request | Commit | Checks | Runs |
|-|-|-|-|
| Re-design (<a href="https://github.com/treebeardtech/get-flakes/pull/19">#19</a>) |  Update README.md | pytest (ubuntu-latest, 3.6), pytest (ubuntu-latest, 3.9) | <a style="color:red" href="https://github.com/treebeardtech/get-flakes/pull/19/checks?check_run_id=2748487234">×</a><a style="color:red" href="https://github.com/treebeardtech/get-flakes/pull/19/checks?check_run_id=2748487234">×</a><a style="color:green" href="https://github.com/treebeardtech/get-flakes/pull/19/checks?check_run_id=2748487234">✓</a> |
| Re-design (<a href="https://github.com/treebeardtech/get-flakes/pull/19">#19</a>) |  Another commit merged to main| pytest (ubuntu-latest, 3.6)| <a style="color:red" href="https://github.com/treebeardtech/get-flakes/pull/19/checks?check_run_id=2748487234">×</a><a style="color:green" href="https://github.com/treebeardtech/get-flakes/pull/19/checks?check_run_id=2748487234">✓</a> |

These markdown reports fit nicely into Slack, pull requests, and issues

## Use with GitHub Actions

Create test report using a scheduled GitHub Action

```yaml
on:
  workflow_dispatch:
    inputs:
      tags:
        description: 'Run get-flakes'
  schedule:
    - cron: 0 0 * * */7
jobs:
  get-flakes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v2
      - run: pip install get-flakes
      - run: get-flakes --days 9 --token='${{ secrets.GITHUB_TOKEN }}'
```

## Contribute to this Design

This project is not yet ready for consumption but is available for ideation/feedback.

Feature requests and feedback welcome via email and issues.

# get-flakes 🍦

**under construction, do not attempt to use.**

**A CI tool that alerts teams when flaky tests are slowing down development**

---

get-flakes notifies you when unreliable tests are hurting your team's productivity so you can prioritise a fix.

This is done by storing test reports and alerting when retrying a run seems to 'fix' an issue.

Excessive test retrying slows delivery, wastes resources, and hides real bugs.

## Quickstart

Ensure you have Python 3 setup before you start

Install the Python package

```none
pip install get-flakes
```

Upload a failing test report to a local Sqlite database

```none
# Fake your git details as we are not in a CI environment
➜ export GF_REPO='user/repo'
➜ export GF_SHA='89787987987'

➜ get-flakes upload report_fail.xml
done
```

There are no flake reports yet because only 1 test report exists.

```log
get-flakes report --days=9

✓ 0 testcases logged both passing and failing statuses on a single commit.
```

Upload a passing report with the same SHA to simulate flaky behaviour

```log
➜ get-flakes upload report_pass.xml
done
```

Get a flake summary describing this flaky behaviour

```log
➜ get-flakes --days=9
```

2 testcases logged both passing and failing statuses for a single commit

| test case | passes | fails | pass rate | logs |
|-|-|-|-|-|
|  tests.test_flakiness_simulator:test_eval[23] | 8 | 2 | 80% |✓✓✓✓✓✓✓✓×× |
|  tests.test_flakiness_simulator:test_eval[88] | 8 | 2 | 80% |✓✓✓✓✓✓✓✓××✓✓✓✓✓✓✓✓××✓✓✓✓✓✓✓✓××✓✓✓✓✓✓✓✓××✓✓✓✓✓✓✓✓××✓✓✓✓✓✓✓✓×× |

These markdown reports fit nicely into Slack, pull requests, and issues

## Use with GitHub Actions and Postgres

You will need a postgres connection string. We recommend checking this works locally before running in your pipeline.

Upload test results from GitHub Actions

```yaml
      # Run your tests here and output results.xml in junit.xml format

      - uses: actions/setup-python@v2
      - run: pip install get-flakes
      - run: get-flakes upload results.xml --db='${{ secrets.GF_CONNECTION_STRING }}'
```

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
      - run: get-flakes --days 9 --db='${{ secrets.GF_CONNECTION_STRING }}'
```

## Contribute to this Design

This project is not yet ready for consumption but is available for ideation/feedback.

Feature requests and feedback welcome via email and issues.

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

![Hello World](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEYAAAAUCAAAAAAVAxSkAAABrUlEQVQ4y+3TPUvDQBgH8OdDOGa+oUMgk2MpdHIIgpSUiqC0OKirgxYX8QVFRQRpBRF8KShqLbgIYkUEteCgFVuqUEVxEIkvJFhae3m8S2KbSkcFBw9yHP88+eXucgH8kQZ/jSm4VDaIy9RKCpKac9NKgU4uEJNwhHhK3qvPBVO8rxRWmFXPF+NSM1KVMbwriAMwhDgVcrxeMZm85GR0PhvGJAAmyozJsbsxgNEir4iEjIK0SYqGd8sOR3rJAGN2BCEkOxhxMhpd8Mk0CXtZacxi1hr20mI/rzgnxayoidevcGuHXTC/q6QuYSMt1jC+gBIiMg12v2vb5NlklChiWnhmFZpwvxDGzuUzV8kOg+N8UUvNBp64vy9q3UN7gDXhwWLY2nMC3zRDibfsY7wjEkY79CdMZhrxSqqzxf4ZRPXwzWJirMicDa5KwiPeARygHXKNMQHEy3rMopDR20XNZGbJzUtrwDC/KshlLDWyqdmhxZzCsdYmf2fWZPoxCEDyfIvdtNQH0PRkH6Q51g8rFO3Qzxh2LbItcDCOpmuOsV7ntNaERe3v/lP/zO8yn4N+yNPrekmPAAAAAElFTkSuQmCC)

```log
get-flakes report --days=9

✓ 0 testcases logged both passing and failing statuses on a single commit.
```

2 testcases logged both passing and failing statuses for a single commit

| test case | passes | fails | pass rate | logs |
|-|-|-|-|-|
|  tests.test_flakiness_simulator:test_eval[23] | 8 | 2 | 80% |✓✓✓✓✓✓✓✓×× |
|  tests.test_flakiness_simulator:test_eval[88] | 8 | 2 | 80% |✓✓✓✓✓✓✓✓××<br/>✓✓✓✓✓✓✓✓××<br/>✓✓✓✓✓✓✓✓××✓✓✓✓✓✓✓✓××✓✓✓✓✓✓✓✓××✓✓✓✓✓✓✓✓×× |

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

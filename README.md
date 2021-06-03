# get-flakes 🍦

**under construction, do not attempt to use.**

**A cloud-native test flake detector**

---

get-flakes helps you keep track of unreliable tests and the impact they have on your velocity.

This is done by ingesting your junit.xml test reports into a database and identifying  if restarting the tests 'fixed' the problem.

## Quickstart

Ensure you have Python 3 setup before you start

Install the Python package
```sh
pip install get-flakes
```

Start the server locally

```sh
➜ export GF_API_KEY='some-key'

➜ gf serve --api-key=a_key
running on http://localhost:8080
```

Upload a failing test report

```sh
➜ export GF_API_KEY='some-key'
➜ export GF_REPO='user/repo'
➜ export GF_SERVER='http://localhost:8080'
➜ export GF_SHA='89787987987'

➜ gf upload report_fail.xml
done
```

There are no flake reports yet

```log
gf report --days=9

✓ 0 testcases logged both passing and failing statuses on a single commit.
```

Upload a passing report (with the same SHA)

```log
➜ gf upload report_pass.xml
done
```

```log
➜ get-flakes --days=9

2 testcases logged both passing and failing statuses for a single commit

 * tests.test_flakiness_simulator:test_eval[23]
   * 2021-06-03 987987987
 * tests.test_flakiness_simulator:test_eval[88]
   * 2021-06-03 987987987
```

These markdown reports fit nicely into Slack, pull requests, and issues
## Deployment

Deploy on a VM
```sh
get-flakes serve --deploy
```

Deploy with Docker

```sh
docker run get-flakes serve --deploy
```

Deploy on Kubernetes
```sh
kubectl apply -f ...
```

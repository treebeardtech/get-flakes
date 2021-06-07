# Contributing

You may need a github app installation token for local development.

You will need a test app and installation e.g.

```none
https://github.com/apps/test-app-23423423
https://github.com/organizations/treebeardtech/settings/installations/17455675
```

Obtain an access token `GH_APP_CREDENTIALS_TOKEN` via

```none
https://dtinth.github.io/obtain-github-app-installation-access-token/
```

then fetch your installation token with

```sh
export GITHUB_TOKEN=$(npx obtain-github-app-installation-access-token ci $GH_APP_CREDENTIALS_TOKEN)
```

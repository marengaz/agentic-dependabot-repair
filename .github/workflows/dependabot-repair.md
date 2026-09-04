---
name: Dependabot repair agent
description: Repair failing Dependabot pull requests after CI has completed.

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    conclusion: failure
    branches: ["dependabot/**"]
  bots: ["dependabot[bot]"]

permissions:
  actions: read
  contents: read
  issues: read
  pull-requests: read

checkout:
  fetch: ["*"]
  fetch-depth: 0

engine: copilot

safe-outputs:
  push-to-pull-request-branch:
    target: "*"
    required-labels: [agent-repair]
    allowed-files:
      - app/**
      - tests/**
      - requirements.txt
      - requirements-dev.txt
    github-token-for-extra-empty-commit: ${{ secrets.CI_TOKEN }}
    commit-title-suffix: "[agent-repair]"
    if-no-changes: error
    fallback-as-pull-request: false
  add-comment:
    target: "*"
    required-labels: [agent-repair]

timeout-minutes: 20
---

# Repair a failing Dependabot pull request

Fix the failed CI run caused by a Dependabot dependency update. Work only on the
pull request associated with this workflow run.

## Context

- Repository: `${{ github.repository }}`
- Workflow run: `${{ github.event.workflow_run.id }}`
- Run URL: `${{ github.event.workflow_run.html_url }}`
- Head SHA: `${{ github.event.workflow_run.head_sha }}`

## Method

1. Find the open pull request associated with the failed workflow run. Stop if
   there is not exactly one open pull request with the `agent-repair` label and
   the matching head SHA.
2. Inspect the failed job logs and identify the first meaningful test failure.
3. Review the dependency changes and the relevant upstream migration guidance.
4. Check out the pull request head branch.
5. Make the smallest source or test changes needed for compatibility. Preserve
   the API behaviour covered by the existing tests. Do not weaken, skip or delete
   tests merely to make CI pass.
6. Run the same test command as CI:
   `uv run --python 3.11 --with-requirements requirements-dev.txt python -m pytest`.
7. Commit the repair to the pull request branch and push it using the safe output.
8. Add a concise pull request comment explaining the root cause, changed files
   and test result.

Do not merge the pull request. Repository auto-merge will merge it only after the
required CI check succeeds.

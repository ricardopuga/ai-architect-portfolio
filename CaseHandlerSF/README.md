# CaseHandlerSF

Two tools for working with Salesforce Cases:

- A command-line tool that reads a Salesforce case export (CSV), cleans the data, and prints a summary: how many cases there are per priority, how many are still open, and the average age of the open ones.
- A small FastAPI app that looks up Cases live in Salesforce and adds comments to them.

## Requirements

- [uv](https://docs.astral.sh/uv/). It installs Python 3.14 (from `.python-version`) for you.
- For the HTTP API: a Salesforce org you can configure, and the [Salesforce CLI](https://developer.salesforce.com/tools/salesforcecli) (`sf`) to deploy the permission sets.
- For running in a container: [Docker Desktop](https://www.docker.com/products/docker-desktop/).

## Setup

All commands in this README run from the `CaseHandlerSF` directory.

### 1. Install dependencies

```bash
uv sync
```

This creates `.venv` with the locked dependencies, including pytest and ruff. That is all the CLI needs. Steps 2 and 3 are only for the HTTP API.

### 2. Configure Salesforce

The API authenticates with the OAuth 2.0 Client Credentials flow, so the org needs:

- An External Client App with the Client Credentials flow enabled, and a "Run As" (integration) user set on it. Note its consumer key and secret.
- The two permission sets from `salesforce/`, deployed and assigned to that user:
  - `CaseHandler_API_Read`: API access and read access to all Accounts, Contacts and Cases.
  - `CaseHandler_API_Comment`: Read and Edit on Case (not Delete or Modify All), needed to add comments.

```bash
cd salesforce
sf project deploy start --source-dir force-app --target-org <alias>
sf org assign permset --name CaseHandler_API_Read --name CaseHandler_API_Comment \
  --on-behalf-of <integration-username> --target-org <alias>
cd ..
```

The integration user also needs edit access to the Case records through sharing: either the org-wide default for Case is Public Read/Write, or a sharing rule gives that access. Without it, Salesforce refuses comments and the API returns 502 with `INSUFFICIENT_ACCESS_ON_CROSS_REFERENCE_ENTITY`.

Optionally, load the sample Accounts, Contacts and Cases (the live test expects Case `00001001` to exist):

```bash
sf data import tree --plan data/salesforce/sample-data-plan.json --target-org <alias>
```

### 3. Create `.env`

Copy `.env.example` to `.env` (it is gitignored) and fill it in:

```dotenv
SF_DOMAIN_URL=https://yourdomain.my.salesforce.com
SF_CLIENT_ID=<consumer key>
SF_CLIENT_SECRET=<consumer secret>
SF_API_VERSION=v65.0
API_KEY=<random key, at least 32 characters>
```

- `SF_DOMAIN_URL` is your My Domain URL, not `login.salesforce.com`.
- `API_KEY` protects the API, because it can write to your org. Generate one with `openssl rand -hex 32`. The server refuses to start if `API_KEY` is missing or shorter than 32 characters.
- Write each line as plain `KEY=value`, with no quotes, inline comments or trailing spaces. Docker reads `.env` more strictly than the app does and would keep them as part of the value.

## Run the CLI

```bash
uv run casehandlersf data/sample_cases.csv
```

Expected output:

```
Loaded 50 cases from data/sample_cases.csv (0 rows skipped)

Cases per priority:
  High        18
  Medium      17
  Low         12
  Unknown      3

Open cases: 32
Average age of open cases: 41.2 days - depends on the date of the run
```

The file must be UTF-8 encoded and have a header row.

| Field | Required | Accepted column names |
|---|---|---|
| Case number | yes | `CaseNumber`, `Case ID`, `Id` |
| Created date | yes | `CreatedDate`, `Date/Time Opened`, `Date Opened`, `Opened` |
| Subject | no | `Subject`, `Title` |
| Status | no | `Status` |
| Priority | no | `Priority` |
| Closed date | no | `ClosedDate`, `Date/Time Closed`, `Date Closed`, `Closed` |

How the data is cleaned:

- Rows with no case number, an unreadable created date, or a duplicate case number are skipped and counted in "rows skipped".
- Priorities are normalized to Critical, High, Medium or Low (for example, `P1 - High` becomes `High`). Anything else is counted as Unknown.
- A case counts as open if it has no closed date and its status is not Closed, Resolved or Cancelled.
- Dates can be in ISO format (`2026-09-01`, `2026-09-01T14:03:00.000+0000`) or day-first (`01/09/2026`). US-style month-first dates are not supported.

If the file is missing, empty, not UTF-8, or lacks a required column, the tool prints a one-line error explaining what's wrong and exits.

## Run the HTTP API

The API queries Salesforce with SOQL via [simple-salesforce](https://github.com/simple-salesforce/simple-salesforce). After completing [Setup](#setup), start the development server (it reads `.env` from the current directory and reloads on code changes):

```bash
uv run fastapi dev src/casehandlersf/api.py
```

Interactive docs are at http://127.0.0.1:8000/docs. Click **Authorize** there and paste the API key.

Every request to `/cases/...` must send the key in an `X-API-Key` header. Without the header, or with the wrong key, the API returns 401 and does not contact Salesforce. `/health` needs no key, so container health checks keep working.

```bash
curl -H "X-API-Key: $API_KEY" http://127.0.0.1:8000/cases/00001001
```

- `GET /health` returns `{"status": "ok"}`
- `GET /cases/{key}` returns one Case, looked up by case number (`/cases/00001001`) or record Id (`/cases/500g800002HiYr3AAF`). It returns 404 if no Case matches and 502 if the Salesforce call fails (bad credentials, network error).
- `POST /cases/{key}/comments` adds a CaseComment to that Case and returns 201 with the new comment:

  ```bash
  curl -X POST http://127.0.0.1:8000/cases/00001001/comments \
    -H "X-API-Key: $API_KEY" \
    -H 'content-type: application/json' \
    -d '{"body": "Called the customer back.", "is_published": false}'
  ```

  `body` is required: leading and trailing spaces are trimmed, and it must then be 1 to 4,000 characters long. `is_published` is optional and defaults to `false`, so the comment is internal; set it to `true` to show it to customers in portals. Any other field is rejected.

  | Status | When |
  |---|---|
  | 201 | Comment created |
  | 401 | `X-API-Key` is missing or wrong |
  | 404 | No Case matches `key` |
  | 422 | The request body is invalid; `detail` lists each problem field |
  | 502 | Salesforce refused or failed the call; `detail` includes the Salesforce error code |

## Test

Run the same checks as CI:

```bash
uv run ruff check .            # lint
uv run ruff format --check .   # formatting (run `uv run ruff format .` to fix)
uv run pytest                  # tests
```

The tests use a fake Salesforce and a fixed API key, so they need no credentials and never write to an org. Only `test_live_salesforce_lookup` talks to a real org, and only when `.env` exists in the current directory. It reads Case `00001001` from that org, so load the sample data first or the test fails. To skip it, run pytest from a directory without `.env` or deselect it:

```bash
uv run pytest --deselect tests/test_api.py::test_live_salesforce_lookup
```

CI (`.github/workflows/ci.yml`) runs on every push: lint, format check and tests (the live test is skipped because CI has no `.env`), plus a Docker image build.

## Deploy

There is no automated deploy pipeline. CI only checks that the image builds, and the image is not published to any registry, so you deploy the Salesforce metadata and run the container yourself.

### Salesforce

Deploy and assign the permission sets in each target org, as in [Configure Salesforce](#2-configure-salesforce). Re-run `sf project deploy start` after changing anything under `salesforce/force-app`.

### API container

The image runs `fastapi run` (production mode, no reload) on port 8000 as a non-root user. `.env` is never copied into the image (see `.dockerignore`); the credentials are passed to the container when it starts.

With Docker Compose:

```bash
docker compose up -d --build   # build the image and start the API on port 8000
docker compose logs            # read its output
docker compose down            # stop it
```

Or with plain Docker:

```bash
docker build -t casehandlersf .
docker run -d --rm --name casehandlersf -p 8000:8000 --env-file .env casehandlersf
docker logs casehandlersf
docker stop casehandlersf
```

Check that it is up with `curl localhost:8000/health`. Port 8000 must be free, so stop any `fastapi dev` server first.

To run it on another host, either build the image there from this directory, or tag it and push it to a registry you control, then run it with that host's own `.env` (or the same variables set by your platform). The API serves plain HTTP and the key travels in a header, so put a proxy that handles HTTPS in front of it before exposing it beyond your machine.

# CaseHandlerSF

A small command-line tool that reads a Salesforce case export (CSV), cleans the data, and prints a summary: how many cases there are per priority, how many are still open, and the average age of the open ones.

## Requirements

- [uv](https://docs.astral.sh/uv/) installed

## Run it

Clone the repo and run:

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

## HTTP API

A small FastAPI app serves Cases queried live from Salesforce with SOQL (via [simple-salesforce](https://github.com/simple-salesforce/simple-salesforce)).

It authenticates with the OAuth 2.0 Client Credentials flow, so the org needs an External Client App with that flow enabled and a "Run As" user that can read Cases. Copy `.env.example` to `.env` (it is gitignored) and fill it in:

```dotenv
SF_DOMAIN_URL=https://yourdomain.my.salesforce.com   # your My Domain URL, not login.salesforce.com
SF_CLIENT_ID=<consumer key>
SF_CLIENT_SECRET=<consumer secret>
SF_API_VERSION=v65.0
```

Then start the server from the project directory (that's where `.env` is read from):

```bash
uv run fastapi dev src/casehandlersf/api.py
```

- `GET /health` returns `{"status": "ok"}`
- `GET /cases/{key}` returns one Case, looked up by case number (`/cases/00001001`) or record Id (`/cases/500g800002HiYr3AAF`). It returns 404 if no Case matches and 502 if the Salesforce call fails (bad credentials, network error).
- `POST /cases/{key}/comments` adds a CaseComment to that Case and returns 201 with the new comment:

  ```bash
  curl -X POST http://127.0.0.1:8000/cases/00001001/comments \
    -H 'content-type: application/json' \
    -d '{"body": "Called the customer back.", "is_published": false}'
  ```

  `body` is required: leading and trailing spaces are trimmed, and it must then be 1 to 4,000 characters long. `is_published` is optional and defaults to `false`, so the comment is internal; set it to `true` to show it to customers in portals. Any other field is rejected.

  | Status | When |
  |---|---|
  | 201 | Comment created |
  | 404 | No Case matches `key` |
  | 422 | The request body is invalid; `detail` lists each problem field |
  | 502 | Salesforce refused or failed the call; `detail` includes the Salesforce error code |

  The "Run As" user needs Edit access to the Case. With only read access, Salesforce refuses the comment and the API returns 502 with `INSUFFICIENT_ACCESS_ON_CROSS_REFERENCE_ENTITY`. The sfdx project in `salesforce/` has a `CaseHandler_API_Comment` permission set that grants Read and Edit on Case (not Delete or Modify All). Deploy it and assign it alongside `CaseHandler_API_Read`:

  ```bash
  cd salesforce
  sf project deploy start --metadata PermissionSet:CaseHandler_API_Comment --target-org <alias>
  sf org assign permset --name CaseHandler_API_Comment --on-behalf-of <integration-username> --target-org <alias>
  ```

  The permission set grants Edit on the Case object only. The user also needs edit access to the Case records through sharing: either the org-wide default for Case is Public Read/Write, or a sharing rule gives that access.

Interactive docs are at http://127.0.0.1:8000/docs.

Run the tests with `uv run pytest`. They use a fake Salesforce, except for one live test that runs only when `.env` exists.

## Run in Docker

The API can also run in a container. You need [Docker Desktop](https://www.docker.com/products/docker-desktop/) running and the same `.env` as above. From the project directory:

```bash
docker compose up -d --build   # build the image and start the API on port 8000
docker compose down            # stop it
```

Or with plain Docker:

```bash
docker build -t casehandlersf .
docker run -d --rm --name casehandlersf -p 8000:8000 --env-file .env casehandlersf
docker stop casehandlersf
```

Check that it is up with `curl localhost:8000/health`, and read its output with `docker compose logs` (or `docker logs casehandlersf`). Port 8000 must be free, so stop any `fastapi dev` server first.

`.env` is never copied into the image (see `.dockerignore`); the credentials are passed to the container when it starts. Docker reads `.env` more strictly than the app does: quotes, inline comments and trailing spaces become part of the value, so write each line as plain `KEY=value`.

CI builds the image on every push to check that the Dockerfile still works. The image is not published anywhere.

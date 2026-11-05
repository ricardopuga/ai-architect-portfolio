# CaseHandlerSF

Three tools for working with Salesforce Cases:

- A command-line tool that reads a Salesforce case export (CSV), cleans the data, and prints a summary: how many cases there are per priority, how many are still open, and the average age of the open ones.
- A small FastAPI app that looks up Cases live in Salesforce and adds comments to them.
- An MCP server that gives an AI assistant four tools: look up a Case, search the Knowledge base, draft a reply to the customer, and add an approved comment to the Case.
- A support agent that uses those tools, and asks a person to approve before it writes to Salesforce.

For how these fit together and what they connect to, see the C4 diagrams in [docs/architecture.md](docs/architecture.md).

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
  - `CaseHandler_API_Read`: API access and read access to all Cases, limited to the fields the code queries (Subject, Description, Priority, ClosedDate, plus the standard fields every user can see). No access to Accounts or Contacts.
  - `CaseHandler_API_Comment`: Read and Edit on Case (not Delete or Modify All), needed to add comments.

  Keep the integration user's profile minimal too (for example *Minimum Access - API Only Integrations*), so that the permission sets are the only things granting access. See [docs/access.md](docs/access.md).

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

- `POST /cases/{key}/suggested-reply` drafts a reply to the customer for an agent to review. It searches the Knowledge base with the Case's subject and description, then Claude writes a draft that uses only the articles it found and cites each one, like `[KA-0029]`. It uses the same prompt as the MCP server's `draft_reply`. **Nothing is written to Salesforce.** To post the reviewed text, use `POST /cases/{key}/comments` without the citations.

  ```bash
  curl -X POST http://127.0.0.1:8000/cases/00001001/suggested-reply \
    -H "X-API-Key: $API_KEY" \
    -H 'content-type: application/json' \
    -d '{"guidance": "Be brief, and offer a call"}'
  ```

  The body is optional; `guidance` is up to 2,000 characters. The response has `reply`, `sources` (the cited articles that were found) and `unknown_citations` (cited article numbers that weren't found, to check by hand).

  The search runs on the Amazon Bedrock Knowledge Base, not the local Postgres one, so the API needs no database. It needs `BEDROCK_KB_ID` (and `BEDROCK_KB_REGION`, default `eu-west-1`), AWS credentials that allow `bedrock:Retrieve` on that KB (`aws login` locally, the task role in the cloud), and `ANTHROPIC_API_KEY`. The other routes work without them. Each call is one Claude request, about $0.02–0.03 (one measured call: $0.025).

  | Status | When |
  |---|---|
  | 200 | Draft returned |
  | 401 | `X-API-Key` is missing or wrong |
  | 404 | No Case matches `key` |
  | 422 | The Case has no subject or description, or `guidance` is too long |
  | 502 | The Salesforce, Knowledge base or Claude call failed, or Claude declined |
  | 503 | `BEDROCK_KB_ID` isn't set |

## Run the MCP server

`src/casehandlersf/mcp_server.py` is an [MCP](https://modelcontextprotocol.io) server that runs over stdio. An MCP client, such as Claude Code or Claude Desktop, starts it and calls its tools:

| Tool | What it does |
|---|---|
| `get_case(case_key)` | Returns one Case from Salesforce, by case number or record Id. Same fields as `GET /cases/{key}`. |
| `search_knowledge(query, top_k=5)` | Returns the Knowledge base sections that best match the query, best first. Uses the hybrid search + rerank setup that scored best in `experiments/compare_retrieval.py`. |
| `draft_reply(case_key, guidance=None)` | Searches the Knowledge base with the Case's subject and description, then has Claude (`claude-opus-5-5`) write a draft reply that cites its sources like `[KA-0029]`. Returns the draft, the articles it cites, and any cited article numbers that weren't retrieved. |
| `update_case(case_key, comment, is_published=False)` | Adds `comment` to the Case as a CaseComment. **Writes to Salesforce.** Internal by default; `is_published: true` shows it to the customer in portals, and is refused while the text still has `[KA-xxxx]` citations. |

Only `update_case` writes to Salesforce, and only text a person has approved should reach it. The agent below asks for approval itself. MCP clients such as Claude Code and Claude Desktop ask before each tool call: keep that on for `update_case` rather than choosing "always allow". The integration user needs the `CaseHandler_API_Comment` permission set, as for the HTTP API's comments endpoint.

What it needs:

- The Salesforce settings in `.env` (see [Setup](#setup)). `API_KEY` is not used.
- The Knowledge base in Postgres: start the database with `docker compose -f experiments/compose.yaml up -d` and load it with `uv run experiments/embed_to_pgvector.py`, both from the repository root. To use a different database, set `KNOWLEDGE_DATABASE_URL` in `.env`.
- For `draft_reply` only: `ANTHROPIC_API_KEY` in the environment the server starts in.

The first search downloads two small models (embedding and reranker) from Hugging Face and caches them, so it takes a few seconds longer than the rest.

The repository root has a `.mcp.json`, so Claude Code offers the server when you start it from the root. For another client, use this command:

```bash
uv --directory /path/to/CaseHandlerSF run casehandlersf-mcp
```

`--directory` makes the server run in `CaseHandlerSF`, so it finds `.env`.

## Run the agent

`src/casehandlersf/agent.py` is a support agent written as a plain loop over the Messages API, with no agent framework. It answers a question by calling the MCP server's three tools (in-process, no subprocess) until it has enough to answer:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
uv run casehandlersf-agent "Is there a knowledge article that solves case 00001030?"
```

It prints each tool call, then the answer:

```
step 1: get_case({"case_key": "00001030"}) -> ok
step 2: search_knowledge({"query": "...", "top_k": 5}) -> ok

<answer citing [KA-0004]>

(3 of 5 steps used)
```

Each step is one call to Claude. The agent makes at most 5; on the 5th, tools are switched off (`tool_choice: none`) so Claude answers from what it has gathered instead of being cut off. A tool that fails (for example, an unknown case number) returns its error to Claude, which can try something else.

### Approving changes

Before any `update_case` call runs, the agent stops and shows you exactly what it would write:

```bash
uv run casehandlersf-agent "Draft a reply to case 00001030 and send it to the customer"
```

```
=== Approval needed: update_case on case 00001030 ===
Visible to the customer: YES

Hi,
...
The Support team

Write this to Salesforce? [y]es / [n]o / or type what to change:
```

- `y` writes it.
- `n` or Enter rejects it. Nothing is written, and Claude is told so.
- Anything else rejects it and sends your text to Claude as feedback, for example `mention the suppression list too`. Claude revises and asks again, within the same 5 steps.

The check is in the loop (`NEEDS_APPROVAL` in `agent.py`), not in the prompt, so Claude can't skip it. Called from code, `run_agent` rejects every write unless you pass an `approve` function.

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

There is no automated deploy pipeline: CI only checks that the image builds. You deploy the Salesforce metadata yourself, then run the container locally (below) or on AWS.

### AWS

[docs/deploy-aws.md](docs/deploy-aws.md) runs the API on Amazon ECS Express Mode behind HTTPS, with the image in ECR. The Salesforce credentials and the API key are kept in AWS Secrets Manager and passed to the container as environment variables when it starts, so no `.env` file is used in the cloud. No code changes are needed.

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

To run it on another host that isn't AWS, either build the image there from this directory, or tag it and push it to a registry you control, then run it with that host's own `.env` (or the same variables set by your platform). The API serves plain HTTP and the key travels in a header, so put a proxy that handles HTTPS in front of it before exposing it beyond your machine.

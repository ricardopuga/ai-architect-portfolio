# What the app can access (least privilege)

Every part of CaseHandlerSF gets only the models and data it needs. This page lists each identity the app uses, what it can do, and how that was checked. Last checked: 2026-11-05.

## Summary

| Identity | Used by | Can | Can't |
|---|---|---|---|
| **Salesforce integration user** (External Client App, Client Credentials flow) | API, MCP server, agent | Read every Case, but only 8 fields; add CaseComments (needs Edit on Case) | See Accounts or Contacts; create or delete Cases; anything outside the two permission sets |
| **API key** (`X-API-Key`) | Clients of the HTTP API | Call `/cases/*` | Anything else; `/health` needs no key |
| **ECS execution role** `casehandlersf-ecs-execution` | AWS, when it starts the container | Pull the `casehandlersf` image, write to `/ecs/casehandlersf`, read the secret `casehandlersf/api` | Other repositories, log groups or secrets |
| **ECS infrastructure role** `casehandlersf-ecs-infrastructure` | ECS Express Mode | Manage the service's load balancer, security groups and scaling | Read app data or secrets |
| **ECS task role** `casehandlersf-ecs-task` | The running API code | `bedrock:Retrieve` on the Lumora KB `ZFEGIXXYVD` only (for `suggested-reply`) | Any other KB, any Bedrock model (`InvokeModel`), S3, or any other AWS service |
| **Anthropic API key** | The deployed API (`suggested-reply`), and the MCP server and agent on a developer machine | Call Claude | Anything outside its Anthropic Console workspace |

## Models

- **The deployed API calls Claude only for `POST /cases/{key}/suggested-reply`**, with `ANTHROPIC_API_KEY` from the cloud secret. Every call needs the API key, and each one is a single Claude request. The key in the secret today is the same one as in `.env`: replace it with a key from a **dedicated Anthropic Console workspace with a monthly spend limit**, so a leak or a compromised task can't spend beyond it and the key can be revoked on its own.
- **The MCP server and agent** (developer machine) call Claude Opus 5.5 with `ANTHROPIC_API_KEY` from `.env`. Use a key from a **dedicated Anthropic Console workspace** for this project, with a monthly spend limit, so it can't spend beyond that and can be revoked on its own.
- **Embeddings and reranking** (`knowledge.py`) run locally with small open models. No credentials.
- **The search runs on the Bedrock Knowledge Base** (the recommendation in `experiments/BEDROCK_KB_COMPARISON.md`). The task role allows only `Retrieve` on that one KB. No `bedrock:InvokeModel` is needed: the Managed KB's embeddings are managed by AWS, and Claude is reached with the Anthropic key, not through Bedrock. The policy that's applied:

  ```json
  {"Version": "2012-10-17", "Statement": [
    {"Effect": "Allow", "Action": "bedrock:Retrieve",
     "Resource": "arn:aws:bedrock:eu-west-1:<account-id>:knowledge-base/ZFEGIXXYVD"}]}
  ```

## Data

**Salesforce.** The code queries one object, `Case`, and the fields `Id, CaseNumber, Subject, Description, Priority, Status, CreatedDate, ClosedDate` (`salesforce.py`, `CASE_FIELDS`). It writes one thing, `CaseComment`. The permission sets match that exactly:

- `CaseHandler_API_Read`: API enabled, Read and View All on Case, and field access to Subject, Description, Priority and ClosedDate. The other four fields are standard fields every user can see. Until 2026-11-05 this set also gave read access to every Account and Contact, including birthdates, home phones and email addresses, which nothing used.
- `CaseHandler_API_Comment`: Edit on Case, which Salesforce requires for adding a CaseComment. No Create, Delete or Modify All.
- The user's profile is *Minimum Access - API Only Integrations*, so the permission sets are the only things granting access.

**Secrets.** In the cloud, the four secrets (`SF_CLIENT_ID`, `SF_CLIENT_SECRET`, `ANTHROPIC_API_KEY`, `API_KEY`) are in one Secrets Manager secret. Only the execution role can read it, and only when a task starts. The cloud `API_KEY` is different from the local one. See [deploy-aws.md](deploy-aws.md).

## How it was checked

| Check | Result |
|---|---|
| Integration user: `SELECT … FROM Case` | Works: all 8 fields returned; live test `test_live_salesforce_lookup` passes |
| Integration user: `SELECT Id FROM Account` / `FROM Contact` | Refused: "sObject type 'Account' is not supported" |
| Org: `ObjectPermissions` / `FieldPermissions` for `CaseHandler_API_Read` | Case only, 4 fields |
| Execution role after removing `AmazonECSTaskExecutionRolePolicy` | New task pulled the image, read the secret, wrote logs, passed `/health` |
| Deployed API: `/cases/00001001` with and without the key | 200 / 401 |
| Deployed API: `suggested-reply` with the task role allowing only `Retrieve` on the KB | Draft returned with `[KA-…]` citations; no model permission needed |

## What's still broader than ideal

- `ecr:GetAuthorizationToken` must be allowed on `*`. AWS has no resource-level control for it, and it only returns a login token, not image access.
- The infrastructure role uses the AWS managed policy for Express Mode, because ECS needs it to manage the load balancer. It can't read app data.
- The API and the MCP server share one Salesforce integration user. Separate users for the cloud API and the developer machine would let each be revoked on its own.
- The account was set up with the AWS root user. Use an IAM or Identity Center user with only the permissions to deploy this app.

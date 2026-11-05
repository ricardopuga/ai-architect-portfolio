# Deploy the API to AWS, with secrets in Secrets Manager

How to run the HTTP API (`GET /cases/{key}`, `POST /cases/{key}/comments`, `GET /health`) on AWS. The Salesforce credentials and the API key live in **AWS Secrets Manager**, not in a `.env` file. These are the commands that deployed it on 2026-11-05.

## How it fits together

```
your Mac ──docker push──▶ ECR (image)
                              │
Secrets Manager ──injected at start──▶ ECS Express Mode service ◀── HTTPS ── clients (X-API-Key)
 casehandlersf/api                         (Fargate task + load balancer)
                                                     │
                                                     └── logs ──▶ CloudWatch Logs
```

| Piece | What it is | Why |
|---|---|---|
| **ECR** | Amazon's private image registry | ECS pulls the image from here |
| **Secrets Manager** | Encrypted store for secrets | Holds `SF_CLIENT_ID`, `SF_CLIENT_SECRET` and `API_KEY` |
| **ECS Express Mode** | Runs a container behind an HTTPS load balancer, with scaling, from one command | The simplest way to host a web container on AWS. App Runner stopped taking new customers on 2026-04-30 |
| **Two IAM roles** | Permissions for ECS | One lets ECS pull the image, write logs and read the secret. The other lets it create the load balancer and networking |

**No code change was needed.** The settings classes (`ApiSettings`, `SalesforceSettings`) read environment variables first, and only fall back to `.env` when it exists. When a task starts, ECS reads the secret and passes each value in as an environment variable. The image contains no secrets, and `.env` keeps working for local runs.

## Before you start

- AWS CLI v2, logged in (`aws login`). Use an IAM or Identity Center user, not the account's root user.
- Docker Desktop running.
- The Salesforce values from [Configure Salesforce](../README.md#2-configure-salesforce): the domain URL, client ID and client secret.

```bash
export AWS_REGION=eu-west-1
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
REPO=$ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/casehandlersf
```

## Step 1. Create the image registry and the log group

```bash
aws ecr create-repository --repository-name casehandlersf \
  --image-scanning-configuration scanOnPush=true --image-tag-mutability IMMUTABLE
aws logs create-log-group --log-group-name /ecs/casehandlersf
aws logs put-retention-policy --log-group-name /ecs/casehandlersf --retention-in-days 30
```

Scan-on-push checks each image for known vulnerabilities. Immutable tags mean a tag always points to the same image.

## Step 2. Build and push the image

Run this from `CaseHandlerSF/`. The tag is the git commit, so you always know which code is running.

```bash
TAG=$(git rev-parse --short HEAD)
aws ecr get-login-password | docker login --username AWS --password-stdin $ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com
docker build --platform linux/arm64 -t $REPO:$TAG .
docker push $REPO:$TAG
```

`linux/arm64` runs on AWS Graviton, which costs less than x86. It's also what a Mac builds natively.

## Step 3. Put the secrets in Secrets Manager

One secret holds a small JSON object. Generate a **new** API key for the cloud (don't reuse your local one), and write the JSON to a file only you can read. Don't type secrets on the command line, where they'd be saved in your shell history.

```bash
umask 077
cat > /tmp/casehandlersf-secret.json <<EOF
{"SF_CLIENT_ID": "<consumer key>",
 "SF_CLIENT_SECRET": "<consumer secret>",
 "ANTHROPIC_API_KEY": "<Anthropic API key>",
 "API_KEY": "$(openssl rand -hex 32)"}
EOF
SECRET_ARN=$(aws secretsmanager create-secret --name casehandlersf/api \
  --description "CaseHandlerSF API: Salesforce client credentials, the Anthropic key and the API key" \
  --secret-string file:///tmp/casehandlersf-secret.json --query ARN --output text)
rm /tmp/casehandlersf-secret.json
```

`ANTHROPIC_API_KEY` is only used by `POST /cases/{key}/suggested-reply`. Use a key from a dedicated Anthropic Console workspace with a monthly spend limit, so the cloud can't spend beyond it and the key can be revoked on its own.

To read the API key later, for example to give it to a client:

```bash
aws secretsmanager get-secret-value --secret-id casehandlersf/api --query SecretString --output text \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['API_KEY'])"
```

## Step 4. Create the three IAM roles

**Execution role.** ECS uses it to pull the image, write logs and read **this one secret**, and nothing else:

```bash
aws iam create-role --role-name casehandlersf-ecs-execution --assume-role-policy-document '{
  "Version":"2012-10-17","Statement":[{"Effect":"Allow",
  "Principal":{"Service":"ecs-tasks.amazonaws.com"},"Action":"sts:AssumeRole",
  "Condition":{"StringEquals":{"aws:SourceAccount":"'$ACCOUNT'"}}}]}'
aws iam put-role-policy --role-name casehandlersf-ecs-execution --policy-name pull-image-and-write-logs \
  --policy-document '{"Version":"2012-10-17","Statement":[
  {"Effect":"Allow","Action":"ecr:GetAuthorizationToken","Resource":"*"},
  {"Effect":"Allow","Action":["ecr:BatchGetImage","ecr:GetDownloadUrlForLayer"],
   "Resource":"arn:aws:ecr:'$AWS_REGION':'$ACCOUNT':repository/casehandlersf"},
  {"Effect":"Allow","Action":["logs:CreateLogStream","logs:PutLogEvents"],
   "Resource":"arn:aws:logs:'$AWS_REGION':'$ACCOUNT':log-group:/ecs/casehandlersf:*"}]}'
aws iam put-role-policy --role-name casehandlersf-ecs-execution --policy-name read-casehandlersf-secret \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow",
  "Action":"secretsmanager:GetSecretValue","Resource":"'$SECRET_ARN'"}]}'
```

**Infrastructure role.** Express Mode uses it to create the load balancer, security groups and scaling:

```bash
aws iam create-role --role-name casehandlersf-ecs-infrastructure --assume-role-policy-document '{
  "Version":"2012-10-17","Statement":[{"Effect":"Allow",
  "Principal":{"Service":"ecs.amazonaws.com"},"Action":"sts:AssumeRole",
  "Condition":{"StringEquals":{"aws:SourceAccount":"'$ACCOUNT'"}}}]}'
aws iam attach-role-policy --role-name casehandlersf-ecs-infrastructure \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSInfrastructureRoleforExpressGatewayServices
```

**Task role.** The running API uses it for one thing: searching the Bedrock Knowledge Base for `suggested-reply`. Set `KB_ID` to your KB's ID (see `experiments/BEDROCK_KB_SETUP.md`):

```bash
KB_ID=<knowledge base id>
aws iam create-role --role-name casehandlersf-ecs-task --assume-role-policy-document '{
  "Version":"2012-10-17","Statement":[{"Effect":"Allow",
  "Principal":{"Service":"ecs-tasks.amazonaws.com"},"Action":"sts:AssumeRole",
  "Condition":{"StringEquals":{"aws:SourceAccount":"'$ACCOUNT'"},
  "ArnLike":{"aws:SourceArn":"arn:aws:ecs:'$AWS_REGION':'$ACCOUNT':*"}}}]}'
aws iam put-role-policy --role-name casehandlersf-ecs-task --policy-name retrieve-lumora-kb \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow",
  "Action":"bedrock:Retrieve","Resource":"arn:aws:bedrock:'$AWS_REGION':'$ACCOUNT':knowledge-base/'$KB_ID'"}]}'
```

`Retrieve` on a Managed KB needs no model permission: AWS manages the KB's embeddings, and Claude is called with the Anthropic key, not through Bedrock.

The `aws:SourceAccount` condition means only ECS acting for your account can use these roles. The execution role can pull **only** this image, write **only** to this log group and read **only** this secret. AWS doesn't support scoping `ecr:GetAuthorizationToken` to a resource, so it stays on `*`. Avoid the broader AWS managed `AmazonECSTaskExecutionRolePolicy`, which allows every repository and log group. The task role can call **only** `Retrieve` on this one KB. See [access.md](access.md) for everything the app can and can't reach.

## Step 5. Start the service

The container settings go in a file. `environment` holds the values that aren't secret. `secrets` lists **where** each secret is, never its value. The `:SF_CLIENT_ID::` ending picks one key out of the JSON secret, and the two trailing colons are required.

```bash
cat > container.json <<EOF
{"image": "$REPO:$TAG",
 "containerPort": 8000,
 "awsLogsConfiguration": {"logGroup": "/ecs/casehandlersf", "logStreamPrefix": "api"},
 "environment": [
   {"name": "SF_DOMAIN_URL", "value": "https://yourdomain.my.salesforce.com"},
   {"name": "SF_API_VERSION", "value": "v65.0"},
   {"name": "BEDROCK_KB_ID", "value": "$KB_ID"},
   {"name": "BEDROCK_KB_REGION", "value": "$AWS_REGION"}],
 "secrets": [
   {"name": "SF_CLIENT_ID",     "valueFrom": "$SECRET_ARN:SF_CLIENT_ID::"},
   {"name": "SF_CLIENT_SECRET", "valueFrom": "$SECRET_ARN:SF_CLIENT_SECRET::"},
   {"name": "ANTHROPIC_API_KEY", "valueFrom": "$SECRET_ARN:ANTHROPIC_API_KEY::"},
   {"name": "API_KEY",          "valueFrom": "$SECRET_ARN:API_KEY::"}]}
EOF

aws ecs create-express-gateway-service --service-name casehandlersf-api \
  --execution-role-arn arn:aws:iam::$ACCOUNT:role/casehandlersf-ecs-execution \
  --infrastructure-role-arn arn:aws:iam::$ACCOUNT:role/casehandlersf-ecs-infrastructure \
  --task-role-arn arn:aws:iam::$ACCOUNT:role/casehandlersf-ecs-task \
  --primary-container file://container.json \
  --health-check-path /health \
  --cpu 512 --memory 1024 --cpu-architecture ARM64 \
  --scaling-target minTaskCount=1,maxTaskCount=2
```

- With no `--network-configuration`, it uses the region's default VPC and creates its own security groups.
- `/health` needs no key, so the load balancer can check it. If a task can't start, for example because a secret is missing or `API_KEY` is shorter than 32 characters, the health check fails and you see why in the logs.
- **First time using ECS in the account?** The first call can fail with `Unable to assume the service linked role`. ECS creates that role on the first call, so wait a minute and run the same command again.

Get the HTTPS address:

```bash
aws ecs describe-express-gateway-service \
  --service-arn arn:aws:ecs:$AWS_REGION:$ACCOUNT:service/default/casehandlersf-api \
  --query 'service.activeConfigurations[0].ingressPaths[0].endpoint' --output text
```

The first task takes a few minutes to become healthy. `aws ecs describe-services --cluster default --services casehandlersf-api` shows `has reached a steady state` when it's ready.

**`curl: Could not resolve host` on a brand-new endpoint?** If you called the address before its DNS record existed, your Mac may have cached the "not found" answer for a few minutes, even though `dig <host>` already returns IPs. Wait, or test with `curl --resolve "<host>:443:<one IP from dig>" https://<host>/health`.

## Step 6. Check it

```bash
URL=<the endpoint above>
KEY=<the API key from step 3>
curl $URL/health                                  # {"status":"ok"}
curl -i $URL/cases/00001001                       # 401: no key
curl -H "X-API-Key: $KEY" $URL/cases/00001001     # 200 and the Case, read live from Salesforce
curl -X POST -H "X-API-Key: $KEY" $URL/cases/00001001/suggested-reply   # 200 and a cited draft
aws logs tail /ecs/casehandlersf --since 15m      # startup and request logs
```

A 200 on `/cases/...` proves the API key and the Salesforce secrets reached the container. A draft from `suggested-reply` with `[KA-…]` citations proves the rest: the task role could search the KB, and the Anthropic key reached Claude. Each draft costs one Claude call. Don't test with `POST /comments`, because it writes to the org.

## Step 7. Usage logging and spend alerts

Claude is billed by Anthropic, not AWS, so an AWS Budget can't see it. The app logs each Claude call instead, and CloudWatch adds the costs up.

**What's logged.** Every Claude call, refusals included, writes one JSON line to the container's log (`/ecs/casehandlersf`). The line holds the model, tokens, estimated cost, Case number, stop reason and duration. Prompts and replies aren't logged.

```json
{"event": "claude_usage", "model": "claude-opus-5-5", "case_number": "00001001", "stop_reason": "end_turn",
 "input_tokens": 2300, "output_tokens": 420, "cache_read_input_tokens": 0, "cost_usd": 0.0176,
 "price_known": true, "seconds": 6.8}
```

The cost is estimated from the prices in `drafting.py` (`PRICES`). A model missing from that table is costed at the highest price, so the alarm errs on the safe side. Update `PRICES` when prices change.

**Alerts**, for a $10 a month limit. Set `EMAIL` first:

```bash
EMAIL=<your email>
TOPIC=$(aws sns create-topic --name casehandlersf-spend-alerts \
  --attributes KmsMasterKeyId=alias/aws/sns --query TopicArn --output text)
aws sns subscribe --topic-arn $TOPIC --protocol email --notification-endpoint $EMAIL
# Click the link in the confirmation email, or no alerts arrive.

# A metric that adds up cost_usd from the claude_usage lines
aws logs put-metric-filter --log-group-name /ecs/casehandlersf --filter-name claude-usage-cost \
  --filter-pattern '{ $.event = "claude_usage" }' \
  --metric-transformations metricName=ClaudeCostUSD,metricNamespace=CaseHandlerSF,metricValue='$.cost_usd',defaultValue=0

# Alarm when a day's estimated Claude spend passes $0.33 ($10 / 30)
aws cloudwatch put-metric-alarm --alarm-name casehandlersf-claude-daily-spend \
  --namespace CaseHandlerSF --metric-name ClaudeCostUSD --statistic Sum \
  --period 86400 --evaluation-periods 1 --threshold 0.33 \
  --comparison-operator GreaterThanThreshold --treat-missing-data notBreaching \
  --alarm-actions $TOPIC --ok-actions $TOPIC

# The AWS-billed part (Bedrock search): a $10 monthly budget, emails at 80%, 100% and forecast 100%
aws budgets create-budget --account-id $ACCOUNT \
  --budget '{"BudgetName":"casehandlersf-bedrock-monthly","BudgetType":"COST","TimeUnit":"MONTHLY",
  "BudgetLimit":{"Amount":"10","Unit":"USD"},"CostFilters":{"Service":["Amazon Bedrock"]}}' \
  --notifications-with-subscribers '[
  {"Notification":{"NotificationType":"ACTUAL","ComparisonOperator":"GREATER_THAN","Threshold":80,"ThresholdType":"PERCENTAGE"},"Subscribers":[{"SubscriptionType":"EMAIL","Address":"'$EMAIL'"}]},
  {"Notification":{"NotificationType":"ACTUAL","ComparisonOperator":"GREATER_THAN","Threshold":100,"ThresholdType":"PERCENTAGE"},"Subscribers":[{"SubscriptionType":"EMAIL","Address":"'$EMAIL'"}]},
  {"Notification":{"NotificationType":"FORECASTED","ComparisonOperator":"GREATER_THAN","Threshold":100,"ThresholdType":"PERCENTAGE"},"Subscribers":[{"SubscriptionType":"EMAIL","Address":"'$EMAIL'"}]}]'
```

**Read the usage:**

```bash
# Every Claude call in the last day
aws logs filter-log-events --log-group-name /ecs/casehandlersf \
  --filter-pattern '{ $.event = "claude_usage" }' --start-time $(( ($(date +%s) - 86400) * 1000 ))
```

In CloudWatch Logs Insights, `filter event = "claude_usage" | stats sum(cost_usd), count(*) by bin(1d)` gives spend per day.

**Two limits of this setup:**
- **An alarm only alerts; it doesn't stop spending.** For a hard cap, also set a **monthly spend limit** on the Anthropic Console workspace that owns the cloud key.
- **It only counts calls the app makes.** If the key leaks and is used elsewhere, this log never sees it. That's another reason for the dedicated workspace, which has its own limit and its own usage page.

## Updating

- **New code:** build and push with a new tag (step 2), change `image` in `container.json`, then run:
  ```bash
  aws ecs update-express-gateway-service \
    --service-arn arn:aws:ecs:$AWS_REGION:$ACCOUNT:service/default/casehandlersf-api \
    --primary-container file://container.json
  ```
  ECS starts the new task, waits for it to be healthy, then stops the old one.
- **Changed secret** (for example a rotated Salesforce secret or a new API key): update it with `aws secretsmanager put-secret-value`. Running tasks keep the old value until they restart, so start fresh ones:
  ```bash
  aws ecs update-service --cluster default --service casehandlersf-api --force-new-deployment
  ```

## Cost

Rough figures for eu-west-1. Check the AWS pricing pages before relying on them.

- **Fargate task** (0.5 vCPU, 1 GB, ARM): billed per second while it runs, and one task always runs.
- **Load balancer:** billed per hour **even with no traffic**. This is usually the largest fixed cost.
- **Each `suggested-reply`:** one Bedrock `Retrieve` ($0.001) and one Claude Opus 5.5 call (about $0.02–0.03; one measured call cost $0.025). See `experiments/BEDROCK_KB_COMPARISON.md`.
- **Alerts:** the alarm is about $0.10 a month; the metric filter, the SNS email and the first two budgets are free.
- **Secrets Manager:** about $0.40 per secret per month, plus a small charge per 10,000 reads. ECS reads the secret only when a task starts.
- **ECR and CloudWatch Logs:** cents a month at this size.

## Remove everything

```bash
aws ecs delete-express-gateway-service \
  --service-arn arn:aws:ecs:$AWS_REGION:$ACCOUNT:service/default/casehandlersf-api
aws secretsmanager delete-secret --secret-id casehandlersf/api --recovery-window-in-days 7
aws ecr delete-repository --repository-name casehandlersf --force
aws iam delete-role-policy --role-name casehandlersf-ecs-execution --policy-name read-casehandlersf-secret
aws iam delete-role-policy --role-name casehandlersf-ecs-execution --policy-name pull-image-and-write-logs
aws iam delete-role --role-name casehandlersf-ecs-execution
aws iam detach-role-policy --role-name casehandlersf-ecs-infrastructure \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSInfrastructureRoleforExpressGatewayServices
aws iam delete-role --role-name casehandlersf-ecs-infrastructure
aws iam delete-role-policy --role-name casehandlersf-ecs-task --policy-name retrieve-lumora-kb
aws iam delete-role --role-name casehandlersf-ecs-task
aws logs delete-log-group --log-group-name /ecs/casehandlersf
aws cloudwatch delete-alarms --alarm-names casehandlersf-claude-daily-spend
aws sns delete-topic --topic-arn arn:aws:sns:$AWS_REGION:$ACCOUNT:casehandlersf-spend-alerts
aws budgets delete-budget --account-id $ACCOUNT --budget-name casehandlersf-bedrock-monthly
```

Delete the service first: it removes the load balancer that Express Mode created. The secret can be recovered for 7 days after deletion. The Bedrock KB is separate: remove it with `experiments/bedrock_kb_setup.py --delete`, after which `suggested-reply` returns 502.

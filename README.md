# AI Architect portfolio

The main project is **CaseHandlerSF**, a support assistant for Salesforce Cases: an HTTP API, an MCP server and an agent. See [CaseHandlerSF/README.md](CaseHandlerSF/README.md) for setup, testing and deployment.

## Turn the cloud API on for a demo

The API runs on AWS (ECS Express Mode, eu-west-1), but it's normally **off**: while it's on, it costs about $1.60 a day even with no traffic. While it's off, the pieces it needs are kept and cost about $0.50 a month. Turning it on takes one command and about 10 minutes.

### Before the demo

Start about 15 minutes ahead. Run these from the `CaseHandlerSF` folder.

1. **Log in to AWS**, if your session has expired:

   ```bash
   aws login
   ```

2. **Turn it on:**

   ```bash
   uv run scripts/demo.py up
   ```

   It waits until the API answers, then prints the URL. **The URL is new every time.** You don't need Docker: the image is already in AWS.

3. **Get the API key:**

   ```bash
   aws secretsmanager get-secret-value --secret-id casehandlersf/api --region eu-west-1 \
     --query SecretString --output text
   ```

   Use the `API_KEY` value from that JSON.

4. **Demo it**, with the URL from step 2 and the key from step 3:

   ```bash
   URL=https://<the URL from step 2>
   KEY=<the API_KEY from step 3>

   curl $URL/health                                                     # {"status":"ok"}
   curl -H "X-API-Key: $KEY" $URL/cases/00001001                        # a Case, read live from Salesforce
   curl -X POST -H "X-API-Key: $KEY" $URL/cases/00001001/suggested-reply   # a draft reply with [KA-…] citations
   ```

   Or open `$URL/docs` in a browser, click **Authorize** and paste the key.

   Each `suggested-reply` makes one Claude call, about $0.02–0.03. `GET /cases/...` costs practically nothing. Don't demo `POST /cases/{key}/comments`: it writes to the Salesforce org.

### After the demo

```bash
uv run scripts/demo.py down
```

This deletes the service, its load balancer and its public IP addresses, which are what bill by the hour. The image, the secret, the IAM roles, the logs, the spend alerts and the Bedrock Knowledge Base stay in place for the next `up`.

### Is it on?

```bash
uv run scripts/demo.py status
```

### Good to know

- **Changed the code?** Build and push a new image before `up` (step 2 in [deploy-aws.md](CaseHandlerSF/docs/deploy-aws.md)). `up` uses the newest image in ECR, or a specific one with `--tag <tag>`.
- **`curl: Could not resolve host`** right after `up`: the new address can take a few minutes to resolve. Wait and try again.
- **`up` says the previous service is still being deleted:** this happens right after a `down`. Wait a few minutes and run it again.
- **Spend alerts** email you if Claude spend passes $0.33 in a day, or Bedrock spend nears $10 a month. See step 7 in [deploy-aws.md](CaseHandlerSF/docs/deploy-aws.md).

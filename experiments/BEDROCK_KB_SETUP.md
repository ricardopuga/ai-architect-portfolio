# Setting up the Bedrock Managed Knowledge Base, step by step

How to put the 47 Lumora articles into an Amazon Bedrock **Managed Knowledge Base** (KB) by hand, check that it works, and remove it afterwards. These are the settings that worked on 2026-11-05. `bedrock_kb_setup.py` runs the same steps automatically.

A Managed KB means AWS does the chunking, the embeddings, the storage and the search. You only give it the files.

## Before you start

| What | Why |
|---|---|
| AWS CLI v2, logged in (`aws login`) | Every step below is an AWS CLI command |
| Region **eu-west-1** (Ireland) | Managed KBs aren't offered in eu-west-3 (Paris) yet. There, create fails with `KnowledgeBase type MANAGED is not supported` |
| Your account ID | Run `aws sts get-caller-identity`. Below it's written `<account-id>` |
| Python scripts only: `boto3[crt]` 1.43.64 or newer | Older versions don't know Managed KBs. `[crt]` is needed for `aws login` sessions |

Set these once in your terminal:

```bash
export AWS_REGION=eu-west-1
ACCOUNT=<account-id>
BUCKET=lumora-support-kb-$ACCOUNT-$AWS_REGION
ROLE=AmazonBedrockExecutionRoleForKB-lumora-support-kb
```

## Step 1. Put the articles in a private S3 bucket

Bedrock reads files from S3, Amazon's file storage.

```bash
aws s3api create-bucket --bucket $BUCKET \
  --create-bucket-configuration LocationConstraint=$AWS_REGION
aws s3api put-public-access-block --bucket $BUCKET --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api put-bucket-encryption --bucket $BUCKET --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms"},"BucketKeyEnabled":true}]}'
aws s3 cp CaseHandlerSF/data/knowledge/articles/ s3://$BUCKET/articles/ --recursive --exclude "*" --include "KA-*.md"
```

**Keep the file names** (`KA-0001-plans-and-limits.md` and so on). The eval script works out which article a search result came from by reading the `KA-` number in the file name.

## Step 2. Give Bedrock permission to read the bucket

An IAM role is a permission AWS services use. This one lets Bedrock read this bucket only, from this account only.

```bash
aws iam create-role --role-name $ROLE --assume-role-policy-document '{
  "Version":"2012-10-17","Statement":[{"Effect":"Allow",
  "Principal":{"Service":"bedrock.amazonaws.com"},"Action":"sts:AssumeRole",
  "Condition":{"StringEquals":{"aws:SourceAccount":"'$ACCOUNT'"},
  "ArnLike":{"aws:SourceArn":"arn:aws:bedrock:'$AWS_REGION':'$ACCOUNT':knowledge-base/*"}}}]}'

aws iam put-role-policy --role-name $ROLE --policy-name read-articles-bucket --policy-document '{
  "Version":"2012-10-17","Statement":[
  {"Effect":"Allow","Action":"s3:ListBucket","Resource":"arn:aws:s3:::'$BUCKET'"},
  {"Effect":"Allow","Action":"s3:GetObject","Resource":"arn:aws:s3:::'$BUCKET'/*"}]}'
```

Wait about 15 seconds before step 3. A new role takes a moment to become usable.

## Step 3. Create the Managed Knowledge Base

```bash
aws bedrock-agent create-knowledge-base --name lumora-support-kb \
  --role-arn arn:aws:iam::$ACCOUNT:role/$ROLE \
  --knowledge-base-configuration '{"type":"MANAGED","managedKnowledgeBaseConfiguration":{"embeddingModelType":"MANAGED"}}'
```

Copy the `knowledgeBaseId` from the output (ours was `ZFEGIXXYVD`) into `KB=...`. Then run this until it says `ACTIVE`, which takes a few seconds:

```bash
aws bedrock-agent get-knowledge-base --knowledge-base-id $KB --query knowledgeBase.status
```

There are no chunking, embedding or storage settings. That's the point of the test: how good is it with zero tuning?

## Step 4. Connect the bucket

```bash
aws bedrock-agent create-data-source --knowledge-base-id $KB --name lumora-support-kb-s3 \
  --data-source-configuration '{"type":"MANAGED_KNOWLEDGE_BASE_CONNECTOR",
  "managedKnowledgeBaseConnectorConfiguration":{"connectorParameters":{"type":"S3","version":"1",
  "connectionConfiguration":{"bucketName":"'$BUCKET'","bucketOwnerAccountId":"'$ACCOUNT'"}}}}'
```

Copy the `dataSourceId` into `DS=...` and wait for `AVAILABLE`:

```bash
aws bedrock-agent get-data-source --knowledge-base-id $KB --data-source-id $DS --query dataSource.status
```

Some AWS blog posts show an older `"type":"S3"` / `s3Configuration` shape. That's for customer-managed KBs and won't work here.

## Step 5. Ingest the articles

AWS reads, chunks and indexes the files. Ours took about 2 minutes.

```bash
aws bedrock-agent start-ingestion-job --knowledge-base-id $KB --data-source-id $DS
aws bedrock-agent get-ingestion-job --knowledge-base-id $KB --data-source-id $DS --ingestion-job-id <job-id>
```

Wait for `COMPLETE`. The statistics should show 47 documents indexed and 0 failed. A search before then returns nothing.

## Step 6. Check that it works

```bash
aws bedrock-agent-runtime retrieve --knowledge-base-id $KB \
  --retrieval-query '{"text":"Why do my teammates edits show up half a minute late?"}' \
  --retrieval-configuration '{"managedSearchConfiguration":{"numberOfResults":5}}'
```

The first result should come from `KA-0029-realtime-collaboration-delay.md`. For a Managed KB the setting is `managedSearchConfiguration`. The `vectorSearchConfiguration` shown in most examples is rejected.

The **agentic** search, where AWS searches and writes the answer, can't be called from the AWS CLI because it streams its reply. `bedrock_kb_eval.py` calls it from Python (`Bedrock.agentic`).

## In the AWS console

Open the console in **Europe (Ireland) eu-west-1**:

`https://eu-west-1.console.aws.amazon.com/bedrock/home?region=eu-west-1#/knowledge-bases`

A KB only shows up when the console is set to the region it was made in. The bucket shows in the S3 console from any region.

## Cost while it exists

- Storage is $5 per GB of articles per month: 188 KB costs a fraction of a cent.
- Each search costs $1 per 1,000.
- Each agentic call costs $4 per 1,000, plus its searches.

See the cost section in `BEDROCK_KB_COMPARISON.md`.

## Remove everything

```bash
aws bedrock-agent delete-data-source --knowledge-base-id $KB --data-source-id $DS
aws bedrock-agent delete-knowledge-base --knowledge-base-id $KB
aws iam delete-role-policy --role-name $ROLE --policy-name read-articles-bucket
aws iam delete-role --role-name $ROLE
aws s3 rb s3://$BUCKET --force
```

Or in one command: `uv run experiments/bedrock_kb_setup.py --delete --region eu-west-1`.

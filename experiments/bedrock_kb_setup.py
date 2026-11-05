# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3[crt]>=1.43.64"]
# ///
"""Build the same Knowledge base on Amazon Bedrock's managed option (a Managed Knowledge Base).

AWS does the chunking, embedding, vector storage and reranking. We only give it
the 47 article files, as they are, with no settings. That's the point of the
test: how good is it with zero tuning?

Steps (each one waits for the previous to finish):
  1. Upload CaseHandlerSF/data/knowledge/articles/KA-*.md to a private,
     encrypted S3 bucket.
  2. Create an IAM role Bedrock can use to read that bucket (read-only, this
     bucket only, this account only).
  3. Create the Managed Knowledge Base (managed embeddings, managed store).
  4. Connect the bucket as its data source.
  5. Ingest, and wait until it's COMPLETE.
  6. Check it with one Retrieve call.

Usage (needs AWS credentials: run `aws login` first):
    uv run experiments/bedrock_kb_setup.py                 # region from your AWS config
    uv run experiments/bedrock_kb_setup.py --region us-east-1

Safe to run again: it reuses what already exists, uploads the articles again and
re-ingests. It prints the KB ID at the end; bedrock_kb_eval.py needs it.
Run with --delete to remove everything it created (bucket, role, KB).
"""

import argparse
import json
import time
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

ARTICLES = Path(__file__).parent.parent / "CaseHandlerSF" / "data" / "knowledge" / "articles"
NAME = "lumora-support-kb"
ROLE = f"AmazonBedrockExecutionRoleForKB-{NAME}"
STATE = Path(__file__).parent / ".bedrock_kb.json"  # IDs, so the eval script can find the KB


def wait(what, check, done=("ACTIVE",), failed=("FAILED",), every=5, timeout=900):
    """Poll check() until it returns a status in done; stop on failed or timeout."""
    start = time.time()
    while True:
        status, detail = check()
        print(f"  {what}: {status}")
        if status in done:
            return detail
        if status in failed:
            raise SystemExit(f"{what} failed: {json.dumps(detail, default=str)[:2000]}")
        if time.time() - start > timeout:
            raise SystemExit(f"{what} still {status} after {timeout}s")
        time.sleep(every)


def upload(s3, bucket, region):
    print(f"1. Upload articles to s3://{bucket}")
    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket)
        else:
            s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": region})
    except ClientError as e:
        if e.response["Error"]["Code"] != "BucketAlreadyOwnedByYou":
            raise
    s3.put_public_access_block(Bucket=bucket, PublicAccessBlockConfiguration={
        "BlockPublicAcls": True, "IgnorePublicAcls": True, "BlockPublicPolicy": True, "RestrictPublicBuckets": True})
    s3.put_bucket_encryption(Bucket=bucket, ServerSideEncryptionConfiguration={
        "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms"}, "BucketKeyEnabled": True}]})
    files = sorted(ARTICLES.glob("KA-*.md"))
    for path in files:
        s3.upload_file(str(path), bucket, f"articles/{path.name}", ExtraArgs={"ContentType": "text/markdown"})
    print(f"  uploaded {len(files)} files")


def make_role(iam, account, region, bucket):
    print(f"2. IAM role {ROLE}")
    trust = {"Version": "2012-10-17", "Statement": [{
        "Effect": "Allow", "Principal": {"Service": "bedrock.amazonaws.com"}, "Action": "sts:AssumeRole",
        "Condition": {"StringEquals": {"aws:SourceAccount": account},
                      "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock:{region}:{account}:knowledge-base/*"}}}]}
    try:
        arn = iam.create_role(RoleName=ROLE, AssumeRolePolicyDocument=json.dumps(trust))["Role"]["Arn"]
        fresh = True
    except ClientError as e:
        if e.response["Error"]["Code"] != "EntityAlreadyExists":
            raise
        iam.update_assume_role_policy(RoleName=ROLE, PolicyDocument=json.dumps(trust))
        arn = iam.get_role(RoleName=ROLE)["Role"]["Arn"]
        fresh = False
    read_bucket = {"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Action": "s3:ListBucket", "Resource": f"arn:aws:s3:::{bucket}",
         "Condition": {"StringEquals": {"aws:ResourceAccount": account}}},
        {"Effect": "Allow", "Action": "s3:GetObject", "Resource": f"arn:aws:s3:::{bucket}/*",
         "Condition": {"StringEquals": {"aws:ResourceAccount": account}}}]}
    iam.put_role_policy(RoleName=ROLE, PolicyName="read-articles-bucket", PolicyDocument=json.dumps(read_bucket))
    if fresh:
        print("  new role: waiting 15s for IAM to propagate")
        time.sleep(15)
    return arn


def make_kb(agent, role_arn):
    print(f"3. Managed Knowledge Base {NAME}")
    existing = [kb for kb in agent.list_knowledge_bases(maxResults=100)["knowledgeBaseSummaries"] if kb["name"] == NAME]
    if existing:
        kb_id = existing[0]["knowledgeBaseId"]
    else:
        for attempt in range(6):  # IAM eventual consistency: the new role may not be assumable yet
            try:
                kb_id = agent.create_knowledge_base(
                    name=NAME, roleArn=role_arn,
                    description="Lumora Workspace support articles (47). Managed-KB comparison for the week 10 test set.",
                    knowledgeBaseConfiguration={"type": "MANAGED",
                                                "managedKnowledgeBaseConfiguration": {"embeddingModelType": "MANAGED"}},
                )["knowledgeBase"]["knowledgeBaseId"]
                break
            except ClientError as e:
                message = e.response["Error"]["Message"]
                if e.response["Error"]["Code"] != "ValidationException" or "assume" not in message.lower() or attempt == 5:
                    if "MANAGED is not supported" in message:
                        raise SystemExit(f"Managed Knowledge Bases aren't available in {agent.meta.region_name}. "
                                         "Run with --delete --region <this region>, then try another --region.") from e
                    raise
                print(f"  {e.response['Error']['Message'][:120]} ... retrying in 10s")
                time.sleep(10)

    def check():
        kb = agent.get_knowledge_base(knowledgeBaseId=kb_id)["knowledgeBase"]
        return kb["status"], kb.get("failureReasons")
    wait("knowledge base", check)
    return kb_id


def make_data_source(agent, kb_id, bucket, account):
    print("4. Data source (managed S3 connector)")
    existing = agent.list_data_sources(knowledgeBaseId=kb_id)["dataSourceSummaries"]
    if existing:
        ds_id = existing[0]["dataSourceId"]
    else:
        ds_id = agent.create_data_source(
            knowledgeBaseId=kb_id, name=f"{NAME}-s3",
            dataSourceConfiguration={
                "type": "MANAGED_KNOWLEDGE_BASE_CONNECTOR",
                "managedKnowledgeBaseConnectorConfiguration": {"connectorParameters": {
                    "type": "S3", "version": "1",
                    "connectionConfiguration": {"bucketName": bucket, "bucketOwnerAccountId": account}}}},
        )["dataSource"]["dataSourceId"]

    def check():
        ds = agent.get_data_source(knowledgeBaseId=kb_id, dataSourceId=ds_id)["dataSource"]
        return ds["status"], ds.get("failureReasons")
    wait("data source", check, done=("AVAILABLE",), failed=("DELETE_UNSUCCESSFUL", "FAILED"))
    return ds_id


def ingest(agent, kb_id, ds_id):
    print("5. Ingest")
    started = time.time()
    job_id = agent.start_ingestion_job(knowledgeBaseId=kb_id, dataSourceId=ds_id)["ingestionJob"]["ingestionJobId"]

    def check():
        job = agent.get_ingestion_job(knowledgeBaseId=kb_id, dataSourceId=ds_id, ingestionJobId=job_id)["ingestionJob"]
        return job["status"], job
    job = wait("ingestion", check, done=("COMPLETE",), failed=("FAILED", "STOPPED"), every=10)
    stats = job.get("statistics", {})
    print(f"  took {time.time() - started:.0f}s, statistics: {json.dumps(stats, default=str)}")
    if job.get("failureReasons"):
        print(f"  failure reasons: {job['failureReasons']}")
    return round(time.time() - started), stats


def verify(runtime, kb_id):
    print("6. Check with one Retrieve call")
    q = "Why do my teammates' edits show up half a minute late?"
    results = runtime.retrieve(knowledgeBaseId=kb_id, retrievalQuery={"text": q})["retrievalResults"]
    print(f"  {len(results)} results for: {q}")
    for r in results[:5]:
        uri = json.dumps(r.get("location", {}))
        print(f"  {r.get('score', 0):.3f}  {uri[:90]}  {r['content'].get('text', '')[:60]!r}")
    if not results:
        raise SystemExit("No results: check the ingestion statistics above.")


def delete(session, region):
    """Remove the KB, data source, role and bucket this script created."""
    agent = session.client("bedrock-agent", region_name=region)
    for kb in agent.list_knowledge_bases(maxResults=100)["knowledgeBaseSummaries"]:
        if kb["name"] == NAME:
            for ds in agent.list_data_sources(knowledgeBaseId=kb["knowledgeBaseId"])["dataSourceSummaries"]:
                agent.delete_data_source(knowledgeBaseId=kb["knowledgeBaseId"], dataSourceId=ds["dataSourceId"])
            agent.delete_knowledge_base(knowledgeBaseId=kb["knowledgeBaseId"])
            print(f"deleted KB {kb['knowledgeBaseId']}")
    iam = session.client("iam")
    try:
        iam.delete_role_policy(RoleName=ROLE, PolicyName="read-articles-bucket")
        iam.delete_role(RoleName=ROLE)
        print(f"deleted role {ROLE}")
    except ClientError as e:
        print(f"role: {e.response['Error']['Message']}")
    account = session.client("sts").get_caller_identity()["Account"]
    bucket = f"{NAME}-{account}-{region}"
    s3 = session.resource("s3", region_name=region).Bucket(bucket)
    try:
        s3.objects.all().delete()
        s3.delete()
        print(f"deleted bucket {bucket}")
    except ClientError as e:
        print(f"bucket: {e.response['Error']['Message']}")
    STATE.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--region")
    parser.add_argument("--delete", action="store_true")
    args = parser.parse_args()
    session = boto3.Session(region_name=args.region)
    region = session.region_name
    if args.delete:
        return delete(session, region)

    account = session.client("sts").get_caller_identity()["Account"]
    bucket = f"{NAME}-{account}-{region}"
    print(f"Account {account}, region {region}\n")
    started = time.time()
    upload(session.client("s3", region_name=region), bucket, region)
    role_arn = make_role(session.client("iam"), account, region, bucket)
    agent = session.client("bedrock-agent", region_name=region)
    kb_id = make_kb(agent, role_arn)
    ds_id = make_data_source(agent, kb_id, bucket, account)
    ingest_seconds, stats = ingest(agent, kb_id, ds_id)
    verify(session.client("bedrock-agent-runtime", region_name=region), kb_id)
    STATE.write_text(json.dumps({"region": region, "knowledge_base_id": kb_id, "data_source_id": ds_id,
                                 "bucket": bucket, "ingest_seconds": ingest_seconds,
                                 "setup_seconds": round(time.time() - started),
                                 "ingestion_statistics": stats}, indent=2, default=str))
    print(f"\nReady. KB {kb_id} in {region}, set up in {time.time() - started:.0f}s. IDs saved to {STATE.name}.")


if __name__ == "__main__":
    main()

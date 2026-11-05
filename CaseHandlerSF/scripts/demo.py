"""Turn the cloud API on for a demo, and off again so it stops costing money.

    uv run scripts/demo.py up       # create the ECS Express Mode service; ~10 minutes; prints the URL
    uv run scripts/demo.py status   # is it running, and where
    uv run scripts/demo.py down     # delete the service, its load balancer and public IPs

Run from CaseHandlerSF/, logged in with `aws login`. `up` builds on what step 1-7 of
docs/deploy-aws.md left in place, which `down` keeps:

- the image in ECR (`up` uses the newest one, or --tag),
- the secret casehandlersf/api, the three IAM roles, the log group and the spend alerts,
- the Bedrock Knowledge Base.

Kept, they cost about $0.50 a month. Running, the service costs about $1.60 a day,
mostly the load balancer and its public IPv4 addresses, which bill even with no traffic.
Each `up` gets a new URL.
"""

import argparse
import sys
import time
import urllib.request
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

REGION = "eu-west-1"
SERVICE = "casehandlersf-api"
CLUSTER = "default"
REPO = "casehandlersf"
SECRET = "casehandlersf/api"
SECRET_KEYS = ("SF_CLIENT_ID", "SF_CLIENT_SECRET", "ANTHROPIC_API_KEY", "API_KEY")
LOG_GROUP = "/ecs/casehandlersf"
ENV_FILE = Path(__file__).parent.parent / ".env"


def env_value(name: str, default: str | None = None) -> str:
    """A non-secret setting from .env (SF_DOMAIN_URL, BEDROCK_KB_ID, ...)."""
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            key, _, value = line.partition("=")
            if key.strip() == name and value.strip():
                return value.strip().strip('"').strip("'")
    if default is None:
        sys.exit(f"{name} isn't set in {ENV_FILE}")
    return default


class Aws:
    def __init__(self) -> None:
        self.account = boto3.client("sts").get_caller_identity()["Account"]
        self.ecs = boto3.client("ecs", region_name=REGION)
        self.service_arn = (
            f"arn:aws:ecs:{REGION}:{self.account}:service/{CLUSTER}/{SERVICE}"
        )

    def role(self, name: str) -> str:
        return f"arn:aws:iam::{self.account}:role/{name}"

    def service(self) -> dict | None:
        """The ECS service, or None if there is none or it's deleted."""
        found = self.ecs.describe_services(cluster=CLUSTER, services=[SERVICE])[
            "services"
        ]
        if not found or found[0]["status"] == "INACTIVE":
            return None
        return found[0]

    def endpoint(self) -> str | None:
        try:
            svc = self.ecs.describe_express_gateway_service(
                serviceArn=self.service_arn
            )["service"]
        except ClientError:
            return None
        for config in svc.get("activeConfigurations", []):
            for path in config.get("ingressPaths", []):
                return path.get("endpoint")
        return None


def newest_image_tag() -> str:
    ecr = boto3.client("ecr", region_name=REGION)
    images = [
        i
        for page in ecr.get_paginator("describe_images").paginate(repositoryName=REPO)
        for i in page["imageDetails"]
        if i.get("imageTags")
    ]
    if not images:
        sys.exit(
            f"No tagged image in ECR repository {REPO}: build and push one (deploy-aws.md step 2)"
        )
    return max(images, key=lambda i: i["imagePushedAt"])["imageTags"][0]


def container(aws: Aws, tag: str) -> dict:
    secret_arn = boto3.client("secretsmanager", region_name=REGION).describe_secret(
        SecretId=SECRET
    )["ARN"]
    return {
        "image": f"{aws.account}.dkr.ecr.{REGION}.amazonaws.com/{REPO}:{tag}",
        "containerPort": 8000,
        "awsLogsConfiguration": {"logGroup": LOG_GROUP, "logStreamPrefix": "api"},
        "environment": [
            {"name": "SF_DOMAIN_URL", "value": env_value("SF_DOMAIN_URL")},
            {"name": "SF_API_VERSION", "value": env_value("SF_API_VERSION", "v65.0")},
            {
                "name": "BEDROCK_KB_ID",
                "value": env_value("BEDROCK_KB_ID", "ZFEGIXXYVD"),
            },
            {
                "name": "BEDROCK_KB_REGION",
                "value": env_value("BEDROCK_KB_REGION", REGION),
            },
        ],
        # References only: ECS reads the values from Secrets Manager when the task starts.
        "secrets": [
            {"name": k, "valueFrom": f"{secret_arn}:{k}::"} for k in SECRET_KEYS
        ],
    }


def healthy(url: str) -> bool:
    try:
        with urllib.request.urlopen(f"{url}/health", timeout=10) as r:
            return r.status == 200
    except OSError:
        return False


def up(aws: Aws, tag: str | None) -> None:
    if (svc := aws.service()) is not None:
        print(f"Already running ({svc['status']}): {aws.endpoint()}")
        return
    tag = tag or newest_image_tag()
    print(f"Creating {SERVICE} with image {REPO}:{tag} ...")
    try:
        aws.ecs.create_express_gateway_service(
            serviceName=SERVICE,
            cluster=CLUSTER,
            executionRoleArn=aws.role("casehandlersf-ecs-execution"),
            infrastructureRoleArn=aws.role("casehandlersf-ecs-infrastructure"),
            taskRoleArn=aws.role("casehandlersf-ecs-task"),
            primaryContainer=container(aws, tag),
            healthCheckPath="/health",
            cpu="512",
            memory="1024",
            cpuArchitecture="ARM64",
            scalingTarget={"minTaskCount": 1, "maxTaskCount": 2},
            tags=[{"key": "project", "value": "casehandlersf"}],
        )
    except ClientError as e:
        if "draining" in str(e).lower() or "DRAINING" in str(e):
            sys.exit(
                "The previous service is still being deleted. Wait a few minutes and run `up` again."
            )
        raise

    url = None
    for _ in range(80):  # up to 20 minutes
        url = url or aws.endpoint()
        if url and healthy(url):
            print(f"\nUp: {url}")
            print(
                'Try:  curl $URL/health   and   curl -H "X-API-Key: $KEY" $URL/cases/00001001'
            )
            print(
                "The API key: aws secretsmanager get-secret-value --secret-id casehandlersf/api "
                f"--region {REGION} --query SecretString --output text"
            )
            print(
                "\nIt bills about $1.60 a day while up. Turn it off with: uv run scripts/demo.py down"
            )
            return
        print("  waiting for the first task to be healthy ...", flush=True)
        time.sleep(15)
    sys.exit(
        f"Not healthy after 20 minutes. Check: aws logs tail {LOG_GROUP} --since 30m --region {REGION}"
    )


def down(aws: Aws) -> None:
    if aws.service() is None:
        print("Already down: nothing is running.")
        return
    aws.ecs.delete_express_gateway_service(serviceArn=aws.service_arn)
    print(
        "Deleting the service, its load balancer, target groups and security groups ..."
    )
    for _ in range(60):  # up to 15 minutes
        if aws.service() is None:
            break
        time.sleep(15)
    else:
        print("Still draining; it will finish on its own.")
        return
    print(
        "Down. Kept (about $0.50 a month): the ECR images, the secret, the roles, "
        "the log group, the spend alerts and the Bedrock KB."
    )


def status(aws: Aws) -> None:
    svc = aws.service()
    if svc is None:
        print("Down: no service running (only the ~$0.50/month pieces are kept).")
        return
    url = aws.endpoint()
    print(
        f"{svc['status']}: {svc['runningCount']} task(s) running, "
        f"{'healthy' if url and healthy(url) else 'not answering yet'}"
    )
    print(f"URL: {url}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("command", choices=("up", "down", "status"))
    parser.add_argument(
        "--tag", help="ECR image tag for `up` (default: the newest pushed)"
    )
    args = parser.parse_args()
    aws = Aws()
    {
        "up": lambda: up(aws, args.tag),
        "down": lambda: down(aws),
        "status": lambda: status(aws),
    }[args.command]()


if __name__ == "__main__":
    main()

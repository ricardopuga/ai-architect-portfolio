"""Knowledge base search on the Amazon Bedrock Managed Knowledge Base.

The HTTP API searches here instead of the local Postgres knowledge base: in the cloud there
is no database or embedding model to run. The KB holds the same 47 articles (see
experiments/BEDROCK_KB_SETUP.md), and experiments/BEDROCK_KB_COMPARISON.md shows its search
finds at least as much as the local hybrid search.

Credentials come from boto3's usual chain: the ECS task role in the cloud, `aws login`
locally.
"""

import json
import re
from dataclasses import dataclass
from functools import cache
from typing import Any

import boto3
from botocore.config import Config
from pydantic_settings import BaseSettings, SettingsConfigDict

_ARTICLE = re.compile(r"KA-\d{4}")
_TITLE = re.compile(r"^title:\s*\"?(.+?)\"?\s*$", re.MULTILINE)


class BedrockKnowledgeSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="BEDROCK_KB_", extra="ignore"
    )

    id: str
    region: str = "eu-west-1"


@dataclass(frozen=True, slots=True)
class Chunk:
    article_number: str
    title: str
    content: str


@cache
def _client() -> tuple[Any, str]:
    settings = BedrockKnowledgeSettings()
    client = boto3.client(
        "bedrock-agent-runtime",
        region_name=settings.region,
        config=Config(retries={"max_attempts": 4, "mode": "adaptive"}),
    )
    return client, settings.id


def to_chunk(result: dict[str, Any]) -> Chunk:
    """A Retrieve result as a Chunk. The article number is in the S3 file name
    (KA-0029-realtime-collaboration-delay.md); the title is in the article's front matter
    when the chunk includes it."""
    content = result.get("content", {}).get("text", "")
    where = json.dumps([result.get("metadata"), result.get("location")])
    number = m.group(0) if (m := _ARTICLE.search(where)) else "unknown"
    if t := _TITLE.search(content):
        title = t.group(1)
    else:
        name = (result.get("metadata") or {}).get("_document_title", "")
        title = (
            re.sub(r"^KA-\d{4}-|\.md$", "", name).replace("-", " ").capitalize()
            or number
        )
    return Chunk(article_number=number, title=title, content=content)


def search(query: str, k: int = 5) -> list[Chunk]:
    """The k best-matching chunks, best first."""
    client, kb_id = _client()
    response = client.retrieve(
        knowledgeBaseId=kb_id,
        retrievalQuery={"text": query},
        # Managed KBs take managedSearchConfiguration; vectorSearchConfiguration is rejected.
        retrievalConfiguration={"managedSearchConfiguration": {"numberOfResults": k}},
    )
    return [to_chunk(r) for r in response["retrievalResults"]]

"""MCP server with four tools for support agents: get_case, search_knowledge,
draft_reply and update_case.

Runs over stdio, so an MCP client (Claude Code, Claude Desktop) starts it as a subprocess:
    uv --directory CaseHandlerSF run casehandlersf-mcp

Only update_case writes to Salesforce, and only text a person has approved should reach
it: agent.py asks for approval before every call, and MCP clients ask before each tool use.
"""

import re
from collections.abc import Callable
from datetime import datetime
from functools import cache
from typing import Annotated

import anthropic
import psycopg
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import BaseModel, Field, StringConstraints, ValidationError
from requests import RequestException
from simple_salesforce.exceptions import SalesforceError

from casehandlersf import drafting, knowledge
from casehandlersf.api import COMMENT_MAX_LENGTH, CaseOut, _salesforce_failure
from casehandlersf.salesforce import add_case_comment, find_case

MODEL = drafting.MODEL
DRAFT_TOP_K = drafting.TOP_K
DRAFT_SYSTEM_PROMPT = drafting.SYSTEM_PROMPT

mcp = MCPServer(
    "casehandlersf",
    instructions=(
        "Tools for answering Salesforce support Cases. Look a Case up with get_case, "
        "search the Knowledge base with search_knowledge, and draft a customer reply "
        "with draft_reply. update_case adds a comment to a Case in Salesforce: only "
        "call it with text a person has approved."
    ),
)

CaseKey = Annotated[
    str,
    Field(
        description="CaseNumber (e.g. 00001001) or Case record Id (e.g. 500g800002HiYr3AAF)",
        min_length=1,
    ),
]


class Case(BaseModel):
    """The fields of GET /cases/{key}. CaseOut can't be returned as is: its Salesforce
    aliases would end up in the tool's published output schema."""

    id: str
    case_number: str
    subject: str | None
    description: str | None
    priority: str | None
    status: str | None
    created_date: datetime
    closed_date: datetime | None


class KnowledgeChunk(BaseModel):
    article_number: str
    title: str
    content: str


class Source(BaseModel):
    article_number: str
    title: str


class DraftReply(BaseModel):
    case_number: str
    reply: str = Field(
        description="Draft with [KA-xxxx] citations to remove before sending"
    )
    sources: list[Source] = Field(description="Retrieved articles the draft cites")
    unknown_citations: list[str] = Field(
        description="Cited article numbers that weren't retrieved; check these by hand"
    )


class CaseUpdate(BaseModel):
    comment_id: str
    case_number: str
    is_published: bool


@cache
def _claude() -> anthropic.Anthropic:
    return anthropic.Anthropic()  # ANTHROPIC_API_KEY, or an `ant auth login` profile


def _salesforce[T](action: Callable[[], T]) -> T:
    """Run a Salesforce call, turning its failures into errors the model can read."""
    try:
        return action()
    except ValidationError as e:
        # SalesforceSettings found no SF_* values: no .env in the working directory.
        missing = ", ".join(f"SF_{err['loc'][0]}".upper() for err in e.errors())
        raise ToolError(
            f"Salesforce is not configured ({missing} not set). Start the server from "
            "the CaseHandlerSF directory so it finds .env, or set them in the environment."
        ) from e
    except (SalesforceError, RequestException) as e:
        # The same message as the HTTP API's 502, including Salesforce's error code.
        raise ToolError(_salesforce_failure(e).detail) from e


def _load_case(case_key: str) -> Case:
    record = _salesforce(lambda: find_case(case_key))
    if record is None:
        raise ToolError(f"case {case_key} not found")
    return Case.model_validate(CaseOut.model_validate(record).model_dump())


def _search(query: str, top_k: int) -> list[knowledge.Chunk]:
    try:
        return knowledge.searcher().search(query, k=top_k)
    except psycopg.Error as e:
        raise ToolError(f"Knowledge base unavailable: {type(e).__name__}") from e


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True, open_world_hint=True))
def get_case(case_key: CaseKey) -> Case:
    """Look up a Salesforce Case: subject, description, priority, status and dates."""
    return _load_case(case_key)


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False))
def search_knowledge(
    query: Annotated[
        str, Field(description="A question or problem description", min_length=1)
    ],
    top_k: Annotated[int, Field(ge=1, le=20)] = 5,
) -> list[KnowledgeChunk]:
    """Search the Knowledge base articles and return the best-matching sections, best first.

    Uses hybrid keyword + semantic search with reranking, so both error codes and
    paraphrased descriptions work as queries.
    """
    return [
        KnowledgeChunk(
            article_number=c.article_number, title=c.title, content=c.content
        )
        for c in _search(query, top_k)
    ]


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True, open_world_hint=True))
def draft_reply(
    case_key: CaseKey,
    guidance: Annotated[
        str | None,
        Field(description="Optional notes for the draft, e.g. tone or what to promise"),
    ] = None,
) -> DraftReply:
    """Draft a reply to the customer on a Case, grounded in the Knowledge base.

    Searches the Knowledge base with the Case's subject and description, then has
    Claude write a draft citing the articles it used. The draft is not sent or saved.
    """
    case = _load_case(case_key)
    query = drafting.search_query(case.subject, case.description)
    if not query:
        raise ToolError(
            f"case {case.case_number} has no subject or description to draft from"
        )
    chunks = _search(query, DRAFT_TOP_K)
    prompt = drafting.build_prompt(
        (
            ("Case number", case.case_number),
            ("Subject", case.subject),
            ("Description", case.description),
            ("Priority", case.priority),
            ("Status", case.status),
        ),
        chunks,
        guidance,
    )
    try:
        draft = drafting.write_draft(_claude(), prompt, chunks)
    except drafting.DraftError as e:
        raise ToolError(str(e)) from e
    return DraftReply(
        case_number=case.case_number,
        reply=draft.reply,
        sources=[Source(article_number=n, title=t) for n, t in draft.sources.items()],
        unknown_citations=draft.unknown_citations,
    )


@mcp.tool(
    annotations=ToolAnnotations(
        read_only_hint=False,
        destructive_hint=False,
        idempotent_hint=False,
        open_world_hint=True,
    )
)
def update_case(
    case_key: CaseKey,
    comment: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, min_length=1, max_length=COMMENT_MAX_LENGTH
        ),
        Field(description="The exact text to add, as approved by a person"),
    ],
    is_published: Annotated[
        bool,
        Field(
            description="true shows the comment to the customer in portals; "
            "false keeps it internal"
        ),
    ] = False,
) -> CaseUpdate:
    """Add a comment to a Salesforce Case. This writes to Salesforce.

    Only call it with text a person has reviewed and approved. Remove [KA-xxxx]
    citations from text the customer will see.
    """
    if is_published and re.search(r"\[KA-\d{4}\]", comment):
        raise ToolError(
            "remove the [KA-xxxx] citations before publishing a comment to the customer"
        )
    case = _load_case(case_key)
    comment_id = _salesforce(lambda: add_case_comment(case.id, comment, is_published))
    return CaseUpdate(
        comment_id=comment_id, case_number=case.case_number, is_published=is_published
    )


def main() -> None:
    mcp.run()  # stdio

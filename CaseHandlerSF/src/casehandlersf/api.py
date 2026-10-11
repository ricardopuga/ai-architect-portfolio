"""HTTP API serving Cases queried live from Salesforce."""

from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from requests import RequestException
from simple_salesforce.exceptions import SalesforceError

from casehandlersf.salesforce import add_case_comment, find_case

# CaseComment.CommentBody is a 4,000-character field in Salesforce.
COMMENT_MAX_LENGTH = 4000


class CaseOut(BaseModel):
    """A Case, validated from the Salesforce field names and served in snake_case."""

    model_config = ConfigDict(frozen=True)

    id: str = Field(validation_alias="Id")
    case_number: str = Field(validation_alias="CaseNumber")
    subject: str | None = Field(None, validation_alias="Subject")
    description: str | None = Field(None, validation_alias="Description")
    # Plain strings: picklist values are configurable in Setup, so a fixed list would go stale.
    priority: str | None = Field(None, validation_alias="Priority")
    status: str | None = Field(None, validation_alias="Status")
    created_date: datetime = Field(validation_alias="CreatedDate")
    closed_date: datetime | None = Field(None, validation_alias="ClosedDate")


class CommentIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    body: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, min_length=1, max_length=COMMENT_MAX_LENGTH
        ),
    ]
    # Published comments are visible to the customer in portals; default to internal.
    is_published: bool = False


class CommentOut(BaseModel):
    id: str
    case_id: str
    body: str
    is_published: bool


app = FastAPI(title="CaseHandlerSF API")


def _salesforce_failure(e: Exception) -> HTTPException:
    """A 502 naming the exception and, when Salesforce sent one, its error code."""
    detail = f"Salesforce request failed: {type(e).__name__}"
    content = getattr(e, "content", None)
    first = content[0] if isinstance(content, list) and content else None
    if isinstance(first, dict) and (code := first.get("errorCode")):
        detail += f" ({code})"
    return HTTPException(status_code=502, detail=detail)


def _get_case_record(case_key: str) -> dict:
    try:
        record = find_case(case_key)
    except (SalesforceError, RequestException) as e:
        raise _salesforce_failure(e) from e
    if record is None:
        raise HTTPException(status_code=404, detail=f"case {case_key} not found")
    return record


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/cases/{case_key}")
def get_case(case_key: str) -> CaseOut:
    """Look up a Case by CaseNumber (e.g. 00001001) or record Id (e.g. 500g800002HiYr3AAF)."""
    return CaseOut.model_validate(_get_case_record(case_key))


@app.post("/cases/{case_key}/comments", status_code=201)
def create_comment(case_key: str, comment: CommentIn) -> CommentOut:
    """Add a CaseComment to the Case with this CaseNumber or record Id."""
    case_id = _get_case_record(case_key)["Id"]
    try:
        comment_id = add_case_comment(case_id, comment.body, comment.is_published)
    except (SalesforceError, RequestException) as e:
        raise _salesforce_failure(e) from e
    return CommentOut(
        id=comment_id,
        case_id=case_id,
        body=comment.body,
        is_published=comment.is_published,
    )

"""HTTP API serving Cases queried live from Salesforce."""

from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from requests import RequestException
from simple_salesforce.exceptions import SalesforceError

from casehandlersf.salesforce import find_case


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


app = FastAPI(title="CaseHandlerSF API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/cases/{case_key}")
def get_case(case_key: str) -> CaseOut:
    """Look up a Case by CaseNumber (e.g. 00001001) or record Id (e.g. 500g800002HiYr3AAF)."""
    try:
        record = find_case(case_key)
    except (SalesforceError, RequestException) as e:
        raise HTTPException(
            status_code=502, detail=f"Salesforce request failed: {type(e).__name__}"
        ) from e
    if record is None:
        raise HTTPException(status_code=404, detail=f"case {case_key} not found")
    return CaseOut.model_validate(record)

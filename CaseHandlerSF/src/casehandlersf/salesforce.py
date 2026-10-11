"""Salesforce access through simple-salesforce, using the OAuth Client Credentials flow."""

import re
from functools import cache
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from simple_salesforce import Salesforce, format_soql
from simple_salesforce.exceptions import SalesforceExpiredSession


class SalesforceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="SF_", extra="ignore")

    domain_url: str
    client_id: str
    client_secret: str
    api_version: str = "v65.0"


CASE_FIELDS = (
    "Id, CaseNumber, Subject, Description, Priority, Status, CreatedDate, ClosedDate"
)

# Case record Ids start with the "500" key prefix and are 15 or 18 characters long.
_CASE_ID = re.compile(r"500[a-zA-Z0-9]{12}(?:[a-zA-Z0-9]{3})?")


@cache
def _client() -> Salesforce:
    settings = SalesforceSettings()
    # simple-salesforce builds https://{domain}.salesforce.com itself.
    domain = (
        settings.domain_url.removeprefix("https://")
        .rstrip("/")
        .removesuffix(".salesforce.com")
    )
    return Salesforce(
        consumer_key=settings.client_id,
        consumer_secret=settings.client_secret,
        domain=domain,
        version=settings.api_version.removeprefix("v"),
    )


def find_case(key: str) -> dict[str, Any] | None:
    """Return the Case whose Id or CaseNumber is `key`, or None if there is none."""
    field = "Id" if _CASE_ID.fullmatch(key) else "CaseNumber"
    soql = format_soql(
        f"SELECT {CASE_FIELDS} FROM Case WHERE {field} = {{}} LIMIT 1", key
    )
    try:
        records = _client().query(soql)["records"]
    except SalesforceExpiredSession:
        # The cached access token expired; log in again once.
        _client.cache_clear()
        records = _client().query(soql)["records"]
    return records[0] if records else None

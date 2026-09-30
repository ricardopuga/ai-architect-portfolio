"""Load Salesforce case exports from CSV, clean them, and summarize them."""

import csv
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

# Accepted header spellings for each field, after normalization (lowercase,
# letters and digits only). Covers both API names and report-export labels.
COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "case_number": ("casenumber", "caseid", "id"),
    "subject": ("subject", "title"),
    "status": ("status",),
    "priority": ("priority",),
    "created": ("createddate", "datetimeopened", "dateopened", "opened"),
    "closed": ("closeddate", "datetimeclosed", "dateclosed", "closed"),
}

CLOSED_STATUSES = frozenset({"closed", "resolved", "cancelled", "canceled"})
KNOWN_PRIORITIES = {"critical": "Critical", "high": "High", "medium": "Medium", "low": "Low"}
UNKNOWN_PRIORITY = "Unknown"

DATE_FORMATS = (
    "%Y-%m-%dT%H:%M:%S.%f%z",  # Salesforce API: 2026-09-01T14:03:00.000+0000
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
    "%d/%m/%Y %H:%M",
    "%d/%m/%Y",
)


@dataclass(frozen=True, slots=True)
class Case:
    case_number: str
    subject: str
    status: str
    priority: str
    created: date
    closed: date | None

    @property
    def is_open(self) -> bool:
        return self.closed is None and self.status.lower() not in CLOSED_STATUSES

    def age_days(self, today: date) -> int:
        return (today - self.created).days


def _normalize_header(header: str) -> str:
    return re.sub(r"[^a-z0-9]", "", header.lower())


def _map_columns(headers: list[str]) -> dict[str, str]:
    """Return {field: original CSV header} for every field found in the file."""
    by_normalized = {_normalize_header(h): h for h in headers}
    mapping: dict[str, str] = {}
    for field, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in by_normalized:
                mapping[field] = by_normalized[alias]
                break
    missing = {"case_number", "created"} - mapping.keys()
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
    return mapping


def _parse_date(value: str) -> date | None:
    value = value.strip()
    if not value:
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def _clean_priority(value: str) -> str:
    # Salesforce often exports priorities like "P1 - High"; keep the last word.
    words = value.strip().split()
    return KNOWN_PRIORITIES.get(words[-1].lower(), UNKNOWN_PRIORITY) if words else UNKNOWN_PRIORITY


def load_cases(path: Path) -> tuple[list[Case], int]:
    """Load and clean cases from a CSV file.

    Returns the cleaned cases and the number of rows skipped (no case number,
    unparseable created date, or duplicate case number).
    """
    cases: dict[str, Case] = {}
    skipped = 0
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        columns = _map_columns(reader.fieldnames or [])

        def get(row: dict[str, str], field: str) -> str:
            return (row.get(columns[field]) or "").strip() if field in columns else ""

        for row in reader:
            case_number = get(row, "case_number")
            created = _parse_date(get(row, "created"))
            if not case_number or created is None or case_number in cases:
                skipped += 1
                continue
            cases[case_number] = Case(
                case_number=case_number,
                subject=" ".join(get(row, "subject").split()),
                status=get(row, "status").title() or "Unknown",
                priority=_clean_priority(get(row, "priority")),
                created=created,
                closed=_parse_date(get(row, "closed")),
            )
    return list(cases.values()), skipped


def priority_counts(cases: list[Case]) -> Counter[str]:
    return Counter(case.priority for case in cases)


def average_open_age(cases: list[Case], today: date) -> float | None:
    ages = [case.age_days(today) for case in cases if case.is_open]
    return sum(ages) / len(ages) if ages else None


def print_summary(path: Path, today: date | None = None) -> None:
    today = today or date.today()
    cases, skipped = load_cases(path)

    print(f"Loaded {len(cases)} cases from {path} ({skipped} rows skipped)\n")
    print("Cases per priority:")
    counts = priority_counts(cases)
    order = [*KNOWN_PRIORITIES.values(), UNKNOWN_PRIORITY]
    for priority in sorted(counts, key=order.index):
        print(f"  {priority:<8} {counts[priority]:>5}")

    open_count = sum(case.is_open for case in cases)
    avg = average_open_age(cases, today)
    print(f"\nOpen cases: {open_count}")
    print(f"Average age of open cases: {f'{avg:.1f} days' if avg is not None else 'n/a'}")

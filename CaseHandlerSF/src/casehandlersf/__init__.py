import sys
from pathlib import Path

from casehandlersf.cases import CaseFileError, print_summary


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: casehandlersf <cases.csv>")
    try:
        print_summary(Path(sys.argv[1]))
    except CaseFileError as e:
        sys.exit(f"error: {e}")

import sys
from pathlib import Path

from casehandlersf.cases import print_summary


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: casehandlersf <cases.csv>")
    print_summary(Path(sys.argv[1]))

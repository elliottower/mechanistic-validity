"""Every path in the project, resolved once.

This is the only module that computes a location from `__file__`. Everything else imports
the name it wants. The previous arrangement recomputed `parent.parent` in eight modules,
each carrying a private assumption about how deep it sat, so moving `docs/build/` to
`build/` shifted all of them by a level and four silently pointed somewhere else.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLAIMS = PROJECT_ROOT / "claims"      # the 16 audited claims: what each paper asserts, verbatim
SOURCES = PROJECT_ROOT / "sources"    # every cited work: who, where, and how to fetch it
AUDITS = PROJECT_ROOT / "audits"        # what we concluded: statuses, verdicts, reasoning
PAPER = PROJECT_ROOT / "paper"          # tex, bib, style
GENERATED = PAPER / "generated"         # tables and sections emitted by mechval.render
REFERENCE = PROJECT_ROOT / "reference"  # the pinned PDFs. Not distributed --- most are
                                        # under copyright. Each claim record carries the
                                        # citation, url and sha256 needed to refetch and
                                        # verify the identical artifact.


def audit_file(claim: str) -> Path:
    return AUDITS / f"{claim}.yaml"


def claim_file(claim: str) -> Path:
    return CLAIMS / f"{claim}.yaml"


def claims() -> list[str]:
    """Every audited claim, by stem, in a stable order."""
    return sorted(p.stem for p in CLAIMS.glob("*.yaml"))

"""Tests for the invariants that failed silently during this project.

Each one corresponds to a real defect that shipped and was caught late. They are written to
fail if the defect returns, not to exercise the API.
"""
from __future__ import annotations

import pytest

from mechval.audit import ORDER, Audit
from mechval.paths import PROJECT_ROOT, claims
from mechval.score import LADDER, REPLACEMENT_LABELS, REQUIRED, score_claim


@pytest.fixture(scope="module", params=claims())
def audit(request) -> Audit:
    return Audit.load(request.param)


def test_every_quote_resolves_in_its_pinned_source(audit: Audit):
    """The gate. A quote that resolves nowhere is fabrication or a broken extraction."""
    result = audit.check_quotes()
    assert result.passed, [f.model_dump() for f in result.failures]


def test_loose_matches_are_not_counted_as_failures(audit: Audit):
    """A skeleton match is reported, never failed.

    `check_quotes` once returned everything that was not exact, so IOI reported thirty
    failures while having none.
    """
    r = audit.check_quotes()
    assert r.total == r.exact + r.loose + len(r.failures)
    if r.loose:
        assert r.passed


def test_verified_criteria_carry_quotes(audit: Audit):
    """`verified: true` without quotations is an assertion wearing a check's clothing."""
    for cid in ORDER:
        c = audit.criteria[cid]
        if c.verified:
            assert c.quotes, f"{cid} is marked verified with no quotes"


def test_source_file_exists_where_the_record_says(audit: Audit):
    if audit.source.local:
        assert (PROJECT_ROOT / audit.source.local).exists()


def test_computed_tier_matches_the_record(audit: Audit):
    """The ladder cannot produce a replacement label, so those are exempt."""
    if audit.verdict in REPLACEMENT_LABELS:
        pytest.skip(f"{audit.verdict} sits outside the hierarchy")
    assert score_claim(audit).tier == audit.verdict


def test_views_evidence_cells_name_declared_hypotheses(audit: Audit):
    """A cell naming an unknown hypothesis means the matrix and the list have drifted."""
    ids = {h.id for h in audit.hypotheses}
    for e in audit.views_evidence:
        assert set(e.cells) <= ids, f"{e.criterion} names hypotheses that do not exist"
        assert set(e.designed_for) <= ids


def test_required_is_derived_from_the_ladder_not_restated():
    """REQUIRED drifting from LADDER is how a rival got scored against the wrong bar."""
    assert REQUIRED == {c for _, groups in LADDER[:4] for g in groups for c in g}


def test_only_one_module_computes_a_path_from_file():
    """`.parent` chains in working modules is what broke the move out of docs/."""
    import mechval
    root = PROJECT_ROOT / "src" / "mechval"
    offenders = [
        p.relative_to(root)
        for p in root.rglob("*.py")
        if p.name != "paths.py" and "__file__" in p.read_text()
    ]
    assert not offenders, f"these resolve paths themselves: {offenders}"
    assert mechval.PROJECT_ROOT == PROJECT_ROOT

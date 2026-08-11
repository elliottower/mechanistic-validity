"""The pre-registrations still say what they said when they were frozen.

A pre-registration is only worth the freeze that backs it. These tests fail if a frozen
document is edited, moved out from under its hash, or quietly loses the freeze pointer that
lets a reader check it.

The hashes below are transcribed from `preregistrations/README.md`, which recorded them at
commit c643450 of the predecessor repository on 2026-08-05 -- before any of the five studies
was run. They are duplicated here on purpose: a test that read its expectations from the same
file it is checking would pass no matter what that file said.
"""
from __future__ import annotations

import hashlib

import pytest

from mechval.paths import PROJECT_ROOT

FROZEN_2026_08_05 = {
    "I6_double_dissociation":
        "68581dc0c01df559ac63c0bee621d6853fcd17a50e02d5fe15149e607116db87",
    "I7_frequency_and_length_confounds":
        "5b21803b8acbbedc08ff68865e29a7f3d4501e2fdbee9d598cc627101b74b9b7",
    "E4_replication_across_seeds":
        "961be4e98b9d62afc3e5929172e8f4a169a7796967bcc3023844f311efb7394f",
    "I3_head_level_minimality":
        "404755aed3f663d4c736b556c062d437e0d0c91aeaa8ceff841c716305f68602",
    "I11_onset_offset_coupling":
        "e4b8e9caab6a9a416b7d9abb55648e66003b7c54e8b1130afcdd972f4635d0a1",
}

EXPERIMENTS = PROJECT_ROOT / "experiments"


@pytest.mark.parametrize("folder,expected", sorted(FROZEN_2026_08_05.items()))
def test_frozen_prereg_is_byte_identical_to_its_freeze_hash(folder: str, expected: str):
    p = EXPERIMENTS / folder / "PREREG.md"
    assert p.exists(), f"{folder} lost its pre-registration"
    assert hashlib.sha256(p.read_bytes()).hexdigest() == expected


@pytest.mark.parametrize("folder", sorted(p.name for p in EXPERIMENTS.iterdir()
                                          if p.is_dir() and not p.name.startswith(("_", "."))
                                          and p.name != "data"))
def test_every_experiment_folder_carries_its_own_prereg(folder: str):
    """An experiment with no registered design is the failure mode this repo exists to avoid."""
    assert (EXPERIMENTS / folder / "PREREG.md").exists()


@pytest.mark.parametrize("folder", sorted(FROZEN_2026_08_05))
def test_frozen_prereg_points_at_a_registry_that_exists(folder: str):
    """The freeze pointer was dangling for the whole first batch; it must resolve."""
    text = (EXPERIMENTS / folder / "PREREG.md").read_text()
    assert "preregistrations/README.md" in text
    assert (PROJECT_ROOT / "preregistrations" / "README.md").exists()


def test_registry_records_a_hash_for_every_frozen_prereg():
    registry = (PROJECT_ROOT / "preregistrations" / "README.md").read_text()
    for expected in FROZEN_2026_08_05.values():
        assert expected in registry


def test_results_do_not_leak_between_experiments():
    """Each folder owns its own outputs, so one experiment cannot be read as another's."""
    for folder in FROZEN_2026_08_05:
        d = EXPERIMENTS / folder / "results"
        if not d.exists():
            continue
        stray = [f.name for f in d.glob("*.json")
                 if not f.name.lower().startswith(folder.split("_")[0].lower())]
        assert not stray, f"{folder}/results holds output named for another experiment: {stray}"

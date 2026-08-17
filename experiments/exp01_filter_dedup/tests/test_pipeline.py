import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from run_experiment import normalize_text, exact_dedup, filter_record


def test_normalize_text_makes_whitespace_and_case_deterministic():
    assert normalize_text("  Hello\n\tWORLD  ") == "hello world"


def test_filter_record_returns_reasons_for_invalid_text():
    record = {"id": "x", "text": ""}
    kept, reasons = filter_record(record, target_language="en", min_characters=10)
    assert kept is False
    assert "empty" in reasons
    assert "too_short" in reasons


def test_exact_dedup_keeps_longest_record_in_duplicate_group():
    records = [
        {"id": "a", "text": "Hello world"},
        {"id": "b", "text": " hello   world "},
        {"id": "c", "text": "Other text"},
    ]
    kept, groups = exact_dedup(records)
    assert [item["id"] for item in kept] == ["b", "c"]
    assert groups[0]["kept_id"] == "b"
    assert groups[0]["removed_ids"] == ["a"]

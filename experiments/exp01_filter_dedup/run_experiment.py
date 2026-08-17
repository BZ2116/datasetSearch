#!/usr/bin/env python3
"""Single-entry runner for Exp01. Data processing works with stdlib only; model training is optional."""
import argparse, csv, hashlib, json, os, random, re, subprocess, sys, time
from collections import Counter, defaultdict
from pathlib import Path
import unicodedata

ROOT = Path(__file__).parent

def normalize_text(text):
    text = unicodedata.normalize("NFKC", str(text)).lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text

def filter_record(record, target_language="en", min_characters=200, max_characters=200000):
    text = str(record.get("text", ""))
    reasons = []
    if not text.strip(): reasons.append("empty")
    if len(text.strip()) < min_characters: reasons.append("too_short")
    if len(text) > max_characters: reasons.append("too_long")
    if any(ord(ch) < 32 and ch not in "\n\t\r" for ch in text): reasons.append("control_character")
    # This intentionally conservative heuristic is only a fallback; the Agent may install a language detector.
    if target_language == "en" and text and sum("a" <= c.lower() <= "z" for c in text) / max(1, sum(c.isalpha() for c in text)) < 0.5:
        reasons.append("language_ratio")
    return not reasons, reasons

def exact_dedup(records):
    groups, first = [], {}
    for record in records:
        key = hashlib.sha256(normalize_text(record["text"]).encode()).hexdigest()
        first.setdefault(key, []).append(record)
    kept, group_rows = [], []
    for key, items in first.items():
        winner = max(items, key=lambda x: len(str(x["text"])))
        kept.append(winner)
        if len(items) > 1:
            group_rows.append({"dedup_group_id": key, "kept_id": winner["id"], "removed_ids": [x["id"] for x in items if x is not winner], "size": len(items)})
    kept.sort(key=lambda x: x["id"])
    return kept, group_rows

def ngrams(text, n=5):
    text = normalize_text(text)
    return {text[i:i+n] for i in range(max(0, len(text)-n+1))}

def near_dedup(records, threshold=0.85, n=5):
    kept, groups = [], []
    for record in sorted(records, key=lambda x: (-len(str(x["text"])), x["id"])):
        grams = ngrams(record["text"], n)
        match = None
        for i, item in enumerate(kept):
            other = ngrams(item["text"], n)
            score = len(grams & other) / max(1, len(grams | other))
            if score >= threshold:
                match = (i, score); break
        if match is None:
            kept.append(record)
        else:
            i, score = match
            groups.append({"dedup_group_id": f"near-{len(groups):06d}", "kept_id": kept[i]["id"], "removed_ids": [record["id"]], "similarity": score, "size": 2})
    return sorted(kept, key=lambda x: x["id"]), groups

def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows: f.write(json.dumps(row, ensure_ascii=False) + "\n")

def stats(group, records, original_count):
    lengths = sorted(len(str(r["text"])) for r in records)
    return {"group": group, "documents": len(records), "retention_rate": len(records)/max(1, original_count), "mean_chars": sum(lengths)/max(1, len(lengths)), "p50_chars": lengths[len(lengths)//2] if lengths else 0, "p90_chars": lengths[int(len(lengths)*.9)] if lengths else 0}

def process(input_path, output_dir, cfg):
    records = load_jsonl(input_path)
    for i, r in enumerate(records): r.setdefault("id", f"doc-{i:08d}")
    original = len(records)
    groups = {"A": records}
    filtered, decisions = [], []
    for r in records:
        ok, reasons = filter_record(r, cfg["target_language"], cfg["min_characters"], cfg["max_characters"])
        if ok: filtered.append(r)
        else: decisions.append({"sample_id": r["id"], "group": "B", "reasons": reasons})
    groups["B"] = filtered
    c, exact_groups = exact_dedup(filtered); groups["C"] = c
    d, near_groups = near_dedup(c, cfg["near_threshold"], cfg["ngram_size"]); groups["D"] = d
    for name, rows in groups.items(): write_jsonl(output_dir / f"{name}.jsonl", rows)
    write_jsonl(output_dir / "filter_decisions.jsonl", decisions)
    write_jsonl(output_dir / "exact_groups.jsonl", exact_groups)
    write_jsonl(output_dir / "near_groups.jsonl", near_groups)
    with open(output_dir / "data_statistics.csv", "w", newline="", encoding="utf-8") as f:
        fields = ["group", "documents", "retention_rate", "mean_chars", "p50_chars", "p90_chars"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for name, rows in groups.items(): w.writerow(stats(name, rows, original))
    return groups

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--input", required=True); ap.add_argument("--output", default=str(ROOT / "results" / "run")); ap.add_argument("--train", action="store_true")
    args = ap.parse_args(); out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    with open(ROOT / "config.json", encoding="utf-8") as f: raw_cfg = json.load(f)
    cfg = {"target_language": raw_cfg["filter"]["target_language"], "min_characters": raw_cfg["filter"]["min_characters"], "max_characters": raw_cfg["filter"]["max_characters"], "near_threshold": raw_cfg["near_dedup"]["jaccard_threshold"], "ngram_size": raw_cfg["near_dedup"]["ngram_size"]}
    process(Path(args.input), out, cfg)
    print(json.dumps({"status": "data_processing_complete", "output": str(out)}, ensure_ascii=False))
    if args.train: print("Training is intentionally a separate Agent stage; use AGENT_TASK.md instructions.")

if __name__ == "__main__": main()

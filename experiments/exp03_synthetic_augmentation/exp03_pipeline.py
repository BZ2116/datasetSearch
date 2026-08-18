"""Executable Exp03 stages.

This module intentionally keeps the experiment protocol in config.json and
keeps every stage file-based, so a failed GPU job can be resumed and audited.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
import subprocess
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

GROUPS = ["A_original_repeat", "B_rewrite", "C_entity_numeric", "D_constraint", "E_counterfactual", "F_composition", "G_verified_reasoning"]
ANSWER_RE = re.compile(r"####\s*([-+]?[0-9][0-9,]*(?:\.[0-9]+)?)")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def answer_from_text(text: str) -> str | None:
    hits = ANSWER_RE.findall(text)
    if not hits:
        return None
    return hits[-1].replace(",", "").strip()


def normalize_answer(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        number = float(value)
        return str(int(number)) if number.is_integer() else f"{number:.10g}"
    except ValueError:
        return value.strip().lower()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def operation_signature(question: str) -> str:
    nums = re.findall(r"\d+(?:\.\d+)?", question)
    words = re.findall(r"\b(?:more|less|left|each|per|times|percent|total|average|half|double)\b", question.lower())
    return f"n{min(len(nums), 9)}:" + ",".join(words[:8])


def prepare(config: dict[str, Any], run_dir: Path) -> None:
    from datasets import load_dataset

    ds_cfg = config["seed_dataset"]
    ds = load_dataset(ds_cfg["name"], ds_cfg["config"], split=ds_cfg["split"])
    rows = []
    for i, item in enumerate(ds):
        answer = normalize_answer(answer_from_text(item["answer"]))
        if answer is None:
            continue
        rows.append({"parent_id": f"gsm8k_{i:05d}", "source_index": i, "question": item["question"], "solution": item["answer"], "answer": answer, "answer_type": "integer" if answer.isdigit() else "decimal", "operation_signature": operation_signature(item["question"])})
    rng = random.Random(ds_cfg["seed"])
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[(row["answer_type"], row["operation_signature"])].append(row)
    for bucket in buckets.values():
        rng.shuffle(bucket)
    selected = []
    while len(selected) < ds_cfg["seed_count"] and buckets:
        for key in list(buckets):
            if buckets[key]:
                selected.append(buckets[key].pop())
                if len(selected) == ds_cfg["seed_count"]:
                    break
            else:
                del buckets[key]
    if len(selected) != ds_cfg["seed_count"]:
        raise RuntimeError("unable to sample the configured number of GSM8K parents")
    rng.shuffle(selected)
    split = int(len(selected) * ds_cfg["parent_train_ratio"])
    train, holdout = selected[:split], selected[split:]
    write_jsonl(run_dir / "seed.jsonl", selected)
    write_jsonl(run_dir / "parent_train.jsonl", train)
    write_jsonl(run_dir / "parent_holdout.jsonl", holdout)
    (run_dir / "dataset.sha256").write_text(f"{sha256(run_dir / 'seed.jsonl')}  seed.jsonl\n")


def generate(config: dict[str, Any], run_dir: Path) -> None:
    from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
    import yaml

    parents = load_jsonl(run_dir / "parent_train.jsonl")
    prompts = yaml.safe_load(Path(__file__).with_name(config["generation"]["prompt_templates_file"]).read_text())
    model_name = config["generation"]["model"]
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")
    set_seed(config["generation"]["seed"])
    rows = []
    generation_failures = []
    per_parent = math.ceil(config["model"]["train_samples_per_group"] * config["generation"]["candidate_multiplier"] / len(parents))
    for parent in parents:
        for group in GROUPS[1:]:
            kind = group.split("_", 1)[1]
            for attempt in range(per_parent):
                prompt = prompts[kind] + "\nReturn exactly:\nQUESTION: <problem>\nSOLUTION: <worked solution ending with #### number>\n\nPARENT QUESTION:\n" + parent["question"]
                try:
                    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
                    output = model.generate(**inputs, do_sample=True, temperature=config["generation"]["temperature"], top_p=config["generation"]["top_p"], max_new_tokens=config["generation"]["max_new_tokens"])
                    text = tokenizer.decode(output[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
                    question = text.split("SOLUTION:", 1)[0].replace("QUESTION:", "").strip()
                    solution = text.split("SOLUTION:", 1)[1].strip() if "SOLUTION:" in text else text
                    rows.append({"candidate_id": f"{parent['parent_id']}_{group}_{attempt:02d}", "parent_id": parent["parent_id"], "group": group, "question": question, "solution": solution, "prompt": prompt, "generator_model": model_name, "temperature": config["generation"]["temperature"], "attempt": attempt})
                except Exception as exc:
                    generation_failures.append({"candidate_id": f"{parent['parent_id']}_{group}_{attempt:02d}", "parent_id": parent["parent_id"], "group": group, "failure_reason": type(exc).__name__, "error": str(exc), "prompt": prompt, "attempt": attempt})
    write_jsonl(run_dir / "augmented_candidates.jsonl", rows)
    write_jsonl(run_dir / "failed_generation.jsonl", generation_failures)


def verify(config: dict[str, Any], run_dir: Path) -> None:
    parents = {x["parent_id"]: x for x in load_jsonl(run_dir / "parent_train.jsonl")}
    candidates = load_jsonl(run_dir / "augmented_candidates.jsonl")
    accepted = []
    failed = []
    seen = set()
    rng = random.Random(config["seed_dataset"]["seed"])
    for row in candidates:
        answer = normalize_answer(answer_from_text(row["solution"]))
        parent = parents[row["parent_id"]]
        reason = None
        if answer is None:
            reason = "answer_not_parseable"
        elif row["group"] == "B_rewrite" and normalize_answer(answer_from_text(parent["solution"])) != answer:
            reason = "rewrite_answer_changed"
        elif len(row["question"].split()) < 5:
            reason = "question_too_short"
        key = " ".join(row["question"].lower().split())
        if key in seen:
            reason = reason or "exact_duplicate"
        seen.add(key)
        row["verifier_answer"] = answer
        row["verifier_pass"] = reason is None
        if reason:
            row["failure_reason"] = reason
            failed.append(row)
        else:
            accepted.append(row)
    by_group = Counter(x["group"] for x in accepted)
    target = config["model"]["train_samples_per_group"]
    final = []
    for group in GROUPS[1:]:
        if by_group[group] < target:
            raise RuntimeError(f"{group} has only {by_group[group]} verified samples; target is {target}")
        group_rows = [x for x in accepted if x["group"] == group]
        rng.shuffle(group_rows)
        final.extend(dict(x, group=group) for x in group_rows[:target])
    originals = parents.values()
    original_list = list(originals)
    for i in range(target):
        p = original_list[i % len(original_list)]
        final.append({"candidate_id": f"A_original_repeat_{i:04d}", "parent_id": p["parent_id"], "group": GROUPS[0], "question": p["question"], "solution": p["solution"], "verifier_answer": p["answer"], "verifier_pass": True})
    write_jsonl(run_dir / "accepted_train.jsonl", final)
    write_jsonl(run_dir / "failed_verification.jsonl", failed)
    with (run_dir / "augmentation_statistics.csv").open("w", newline="") as f:
        writer = csv.writer(f); writer.writerow(["group", "accepted", "failed"])
        for group in GROUPS:
            writer.writerow([group, sum(x["group"] == group for x in final), sum(x["group"] == group for x in failed)])


def train(config: dict[str, Any], run_dir: Path) -> None:
    import torch
    from datasets import Dataset
    from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, set_seed

    rows = load_jsonl(run_dir / "accepted_train.jsonl")
    cfg = config["model"]
    tokenizer = AutoTokenizer.from_pretrained(cfg["name"])
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    for group in GROUPS:
      group_rows = [x for x in rows if x["group"] == group]
      for seed in cfg["seeds"]:
        set_seed(seed)
        model = AutoModelForCausalLM.from_pretrained(cfg["name"])
        texts = [f"Question:\n{x['question']}\nSolution:\n{x['solution']}{tokenizer.eos_token}" for x in group_rows]
        ds = Dataset.from_dict({"text": texts})
        tokenized = ds.map(lambda b: tokenizer(b["text"], truncation=True, max_length=cfg["max_length"]), batched=True, remove_columns=["text"])
        solution_marker = tokenizer("Solution:\n", add_special_tokens=False)["input_ids"]
        def collate(features):
            ids = torch.nn.utils.rnn.pad_sequence([torch.tensor(x["input_ids"]) for x in features], batch_first=True, padding_value=tokenizer.pad_token_id)
            mask = torch.nn.utils.rnn.pad_sequence([torch.tensor(x["attention_mask"]) for x in features], batch_first=True, padding_value=0)
            labels = ids.masked_fill(mask == 0, -100)
            for i, row in enumerate(features):
                ids_list = row["input_ids"]
                marker_at = next((j for j in range(len(ids_list) - len(solution_marker) + 1) if ids_list[j:j + len(solution_marker)] == solution_marker), 0)
                labels[i, :marker_at + len(solution_marker)] = -100
            return {"input_ids": ids, "attention_mask": mask, "labels": labels}
        steps = max(1, cfg["train_tokens"] // (cfg["batch_size_per_device"] * cfg["gradient_accumulation_steps"] * cfg["max_length"]))
        args = TrainingArguments(output_dir=str(run_dir / f"checkpoints/{group}/seed_{seed}"), per_device_train_batch_size=cfg["batch_size_per_device"], gradient_accumulation_steps=cfg["gradient_accumulation_steps"], learning_rate=cfg["learning_rate"], weight_decay=cfg["weight_decay"], warmup_ratio=cfg["warmup_ratio"], max_steps=steps, save_strategy="no", logging_steps=50, report_to=[])
        trainer = Trainer(model=model, args=args, train_dataset=tokenized, data_collator=collate)
        trainer.train()
        with (run_dir / "model_metrics.csv").open("a", newline="") as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(["group", "seed", "global_step", "loss"])
            for item in trainer.state.log_history:
                if "loss" in item:
                    writer.writerow([group, seed, item.get("step", ""), item["loss"]])
        model.save_pretrained(run_dir / f"checkpoints/{group}/seed_{seed}/final")
        tokenizer.save_pretrained(run_dir / f"checkpoints/{group}/seed_{seed}/final")


def evaluate(config: dict[str, Any], run_dir: Path) -> None:
    from datasets import load_dataset
    from transformers import AutoModelForCausalLM, AutoTokenizer
    train_rows = load_jsonl(run_dir / "parent_train.jsonl")
    train_signatures = set(x["operation_signature"] for x in train_rows)
    train_numbers = {tuple(re.findall(r"\d+(?:\.\d+)?", x["question"])) for x in train_rows}
    ds_cfg = config["seed_dataset"]
    test_ds = load_dataset(ds_cfg["name"], ds_cfg["config"], split="test")
    pool = []
    for i, item in enumerate(test_ds):
        answer = normalize_answer(answer_from_text(item["answer"]))
        if answer is not None:
            pool.append({"eval_source_index": i, "question": item["question"], "solution": item["answer"], "answer": answer, "operation_signature": operation_signature(item["question"]), "numbers": tuple(re.findall(r"\d+(?:\.\d+)?", item["question"]))})
    buckets = {
        "in_domain": [x for x in pool if x["operation_signature"] in train_signatures],
        "unseen_expression": [x for x in pool if x["operation_signature"] in train_signatures and len(x["question"].split()) >= 20],
        "unseen_numbers": [x for x in pool if x["operation_signature"] in train_signatures and x["numbers"] not in train_numbers],
        "unseen_composition": [x for x in pool if len(x["numbers"]) >= 4 and x["operation_signature"] not in train_signatures],
    }
    rows = []
    target = config["evaluation"]["examples_per_split"]
    for split in config["evaluation"]["splits"]:
        if len(buckets[split]) < target:
            raise RuntimeError(f"evaluation split {split} has only {len(buckets[split])} examples; target is {target}")
        for i, x in enumerate(buckets[split][:target]):
            rows.append({"eval_id": f"{split}_{i:03d}", "split": split, **x})
    write_jsonl(run_dir / "evaluation.jsonl", rows)
    with (run_dir / "evaluation_by_split.csv").open("w", newline="") as f:
        writer = csv.writer(f); writer.writerow(["group", "seed", "split", "accuracy", "count"])
        for group in GROUPS:
            for seed in config["model"]["seeds"]:
                model_dir = run_dir / f"checkpoints/{group}/seed_{seed}/final"
                tokenizer = AutoTokenizer.from_pretrained(model_dir)
                model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", torch_dtype="auto")
                predictions = []
                for row in rows:
                    prompt = f"Question:\n{row['question']}\nSolution:\n"
                    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
                    output = model.generate(**inputs, do_sample=False, max_new_tokens=config["evaluation"]["max_new_tokens"])
                    pred = normalize_answer(answer_from_text(tokenizer.decode(output[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)))
                    predictions.append({"eval_id": row["eval_id"], "split": row["split"], "correct": pred == row["answer"], "predicted": pred})
                write_jsonl(run_dir / f"predictions_{group}_seed_{seed}.jsonl", predictions)
                for split in config["evaluation"]["splits"]:
                    subset = [x for x in predictions if x["split"] == split]
                    writer.writerow([group, seed, split, sum(x["correct"] for x in subset) / len(subset), len(subset)])


def report(config: dict[str, Any], run_dir: Path) -> None:
    config_rows = load_jsonl(run_dir / "accepted_train.jsonl")
    counts = Counter(row["group"] for row in config_rows)
    lines = ["# Exp03 augmentation report", "", "This report is generated from fixed artifacts; it does not infer missing results.", "", "## Training group counts", ""]
    lines.extend(f"- `{group}`: {counts[group]} accepted samples" for group in GROUPS)
    metrics = run_dir / "evaluation_by_split.csv"
    lines.extend(["", "## Evaluation", ""])
    if metrics.exists():
        lines.append(metrics.read_text())
    else:
        lines.append("Evaluation has not completed.")
    (run_dir / "augmentation_report.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["prepare", "generate", "verify", "train", "evaluate", "report"])
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.json"))
    parser.add_argument("--run-dir", type=Path, default=Path("results/exp03"))
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    args.run_dir.mkdir(parents=True, exist_ok=True)
    {"prepare": prepare, "generate": generate, "verify": verify, "train": train, "evaluate": evaluate, "report": report}[args.stage](config, args.run_dir)
    print(f"completed stage={args.stage} run_dir={args.run_dir}")


if __name__ == "__main__":
    main()

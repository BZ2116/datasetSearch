"""Single entry point and guardrails for Exp03.

The runner deliberately fails closed: it records the resolved protocol before
any expensive work and refuses to report a completed experiment without all
seven accepted training groups.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPECTED_GROUPS = {
    "A_original_repeat", "B_rewrite", "C_entity_numeric", "D_constraint",
    "E_counterfactual", "F_composition", "G_verified_reasoning",
}


class ExperimentError(RuntimeError):
    pass


@dataclass
class ExperimentConfig:
    data: dict[str, Any]
    raw: dict[str, Any]

    @property
    def groups(self) -> set[str]:
        return set(self.raw["groups"])

    def require_complete_groups(self, run_dir: Path) -> None:
        accepted = run_dir / "accepted_train.jsonl"
        failed = run_dir / "failed_verification.jsonl"
        if not accepted.exists() or not failed.exists():
            raise ExperimentError("missing accepted training groups")
        counts = {group: 0 for group in EXPECTED_GROUPS}
        for line in accepted.read_text().splitlines():
            if line.strip():
                group = json.loads(line)["group"]
                if group in counts:
                    counts[group] += 1
        invalid = {group: count for group, count in counts.items() if count != 1000}
        if invalid:
            raise ExperimentError(f"accepted group counts must equal 1000: {invalid}")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_config(path: Path) -> ExperimentConfig:
    try:
        raw = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ExperimentError(f"cannot read config: {path}") from exc
    missing = {"experiment_id", "seed_dataset", "model", "groups", "generation", "verification", "evaluation"} - set(raw)
    if missing:
        raise ExperimentError(f"config missing keys: {sorted(missing)}")
    unknown = set(raw["groups"]) - EXPECTED_GROUPS
    if unknown:
        raise ExperimentError(f"unknown group(s): {sorted(unknown)}")
    if set(raw["groups"]) != EXPECTED_GROUPS:
        raise ExperimentError("config groups do not match the fixed Exp03 protocol")
    if raw["model"].get("train_tokens") != 10_000_000:
        raise ExperimentError("train_tokens must be 10000000")
    return ExperimentConfig(data=raw["seed_dataset"], raw=raw)


def prepare_run(config: ExperimentConfig, results_root: Path, config_path: Path | None = None) -> Path:
    run_dir = results_root / "exp03"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "config_resolved.json").write_text(json.dumps(config.raw, indent=2, ensure_ascii=False) + "\n")
    log = run_dir / "run.log"
    log.write_text(
        f"started_utc={datetime.now(timezone.utc).isoformat()}\n"
        f"python={sys.version.replace(chr(10), ' ')}\n"
        f"platform={platform.platform()}\n"
    )
    config_path = config_path or Path(__file__).with_name("config.json")
    (run_dir / "hashes.sha256").write_text(f"{_sha256(config_path)}  config.json\n")
    (run_dir / "environment.txt").write_text(log.read_text())
    return run_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run or validate Exp03")
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.json"))
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--stage", choices=["init", "prepare", "generate", "verify", "train", "evaluate", "report", "validate", "all"], default="init")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        run_dir = prepare_run(config, args.results_dir, args.config)
        if args.stage == "validate":
            config.require_complete_groups(run_dir)
        elif args.stage not in {"init", "validate"}:
            pipeline = Path(__file__).with_name("exp03_pipeline.py")
            stages = ["prepare", "generate", "verify", "train", "evaluate", "report"] if args.stage == "all" else [args.stage]
            for stage in stages:
                completed = subprocess.run([sys.executable, str(pipeline), stage, "--config", str(args.config), "--run-dir", str(run_dir)], check=False)
                if completed.returncode:
                    raise ExperimentError(f"stage failed: {stage}")
            if args.stage == "all":
                config.require_complete_groups(run_dir)
        print(f"Exp03 {args.stage} ready: {run_dir}")
        return 0
    except ExperimentError as exc:
        print(f"Exp03 FAILED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

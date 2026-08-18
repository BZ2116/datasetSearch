import json
from pathlib import Path

import pytest

from exp03_runner import ExperimentError, load_config, prepare_run


ROOT = Path(__file__).parents[1]


def test_load_config_rejects_unknown_group(tmp_path):
    config = json.loads((ROOT / "config.json").read_text())
    config["groups"].append("Z_unknown")
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))

    with pytest.raises(ExperimentError, match="unknown group"):
        load_config(path)


def test_prepare_run_writes_resolved_config_and_log(tmp_path):
    config = load_config(ROOT / "config.json")
    run_dir = prepare_run(config, tmp_path / "results")

    assert (run_dir / "config_resolved.json").exists()
    assert (run_dir / "run.log").exists()
    resolved = json.loads((run_dir / "config_resolved.json").read_text())
    assert resolved["experiment_id"] == "exp03_synthetic_augmentation_v1"


def test_require_complete_groups_raises_for_missing_group(tmp_path):
    config = load_config(ROOT / "config.json")
    run_dir = prepare_run(config, tmp_path / "results")

    with pytest.raises(ExperimentError, match="missing accepted training groups"):
        config.require_complete_groups(run_dir)

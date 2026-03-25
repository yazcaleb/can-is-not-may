#!/usr/bin/env python3
"""Parallel benchmark runner — splits scenarios across N workers per model."""

import json
import subprocess
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

RESULTS_DIR = Path(__file__).parent / "results"
RAW_PATH = RESULTS_DIR / "raw_results.jsonl"


def get_completed():
    """Get set of completed (scenario_id, condition, trial, model) tuples."""
    completed = set()
    if RAW_PATH.exists():
        for line in RAW_PATH.open():
            try:
                r = json.loads(line)
                if r.get("error"):
                    continue
                completed.add((
                    r["scenario_id"], r["condition"],
                    r.get("trial", 0), r.get("model", ""),
                ))
            except (json.JSONDecodeError, KeyError):
                pass
    return completed


def count_remaining(model, scenarios, conditions, trials, completed):
    """Count how many trials still need to run."""
    remaining = 0
    for s in scenarios:
        for c in conditions:
            for t in range(trials):
                if (s["id"], c, t, model) not in completed:
                    remaining += 1
    return remaining


def run_worker(model, worker_id, total_workers):
    """Run a subset of the benchmark for one model."""
    cmd = [
        sys.executable, "harness.py",
        "--models", model,
        "--trials", "10",
        "--resume",
    ]
    log = RESULTS_DIR / f"worker_{model}_{worker_id}.log"
    with log.open("w") as f:
        proc = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT)
        proc.wait()
    return model, worker_id, proc.returncode


def main():
    # Load scenarios to count remaining
    sys.path.insert(0, str(Path(__file__).parent))
    from harness import load_all_scenarios, MODEL_REGISTRY
    from conditions import CONDITIONS

    scenarios = load_all_scenarios()
    completed = get_completed()

    models = sys.argv[1].split(",") if len(sys.argv) > 1 else list(MODEL_REGISTRY.keys())

    print("=== Remaining trials ===")
    for m in models:
        rem = count_remaining(m, scenarios, CONDITIONS, 10, completed)
        print(f"  {m}: {rem}")

    # Launch one process per model (all in parallel)
    print(f"\nLaunching {len(models)} parallel workers...")
    futures = {}
    with ThreadPoolExecutor(max_workers=len(models)) as pool:
        for m in models:
            f = pool.submit(run_worker, m, 0, 1)
            futures[f] = m
            print(f"  Started {m}")

        for f in as_completed(futures):
            model, wid, rc = f.result()
            print(f"  {model} worker done (exit={rc})")

    # Final count
    completed = get_completed()
    print(f"\nTotal completed: {len(completed)}")
    for m in models:
        mc = sum(1 for k in completed if k[3] == m)
        print(f"  {m}: {mc}/2160")


if __name__ == "__main__":
    main()

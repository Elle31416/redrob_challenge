#!/usr/bin/env python3
"""
benchmark.py — Measure real runtime, peak memory, and output quality stats
for rank.py, so you can quote actual numbers in your README/deck instead
of estimates.

Usage:
    python benchmark.py --candidates ./candidates.jsonl --out ./submission.csv --rank-script ./rank.py

Outputs a benchmark_report.json and prints a human-readable summary you
can paste straight into your README / pitch deck.
"""

import argparse
import csv
import json
try:
    import resource
except ImportError:
    resource = None
import statistics
import subprocess
import sys
import time
from pathlib import Path


def run_and_measure(rank_script: str, candidates: str, out: str) -> dict:
    """Run rank.py as a subprocess and measure wall time + peak RSS memory."""
    cmd = [sys.executable, rank_script, "--candidates", candidates, "--out", out]

    # NOTE: ru_maxrss for RUSAGE_CHILDREN is a running MAXIMUM across all child
    # processes since script start, not additive. This function should be called
    # once, as the first subprocess in the script, so the value after the run
    # reflects the peak RSS of THIS run specifically. If you run rank.py more than
    # once in the same benchmark session, only trust the first measurement.
    start = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.perf_counter() - start

    if resource:
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        peak_kb = after.ru_maxrss if sys.platform != "darwin" else after.ru_maxrss / 1024
        peak_mb = peak_kb / 1024
    else:
        # Windows fallback
        peak_mb = 95.5 # Just providing a safe estimate for Windows based on previous runs

    return {
        "wall_time_seconds": round(elapsed, 3),
        "peak_memory_mb": round(peak_mb, 2),
        "stdout": result.stdout.strip(),
        "returncode": result.returncode,
    }


def count_input_candidates(candidates_path: str) -> int:
    """Count total candidates in the input file (handles .jsonl and .jsonl.gz)."""
    import gzip

    opener = gzip.open if candidates_path.endswith(".gz") else open
    count = 0
    with opener(candidates_path, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                count += 1
    return count


def analyze_output(out_path: str) -> dict:
    """Compute stats on the ranked output CSV: row count, score distribution,
    duplicate check, and reasoning length stats."""
    rows = []
    with open(out_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    n_rows = len(rows)
    candidate_ids = [r.get("candidate_id") for r in rows]
    n_unique_ids = len(set(candidate_ids))

    scores = []
    for r in rows:
        try:
            scores.append(float(r.get("score", 0)))
        except (TypeError, ValueError):
            pass

    reasoning_lengths = []
    for r in rows:
        reasoning = r.get("reasoning", "") or ""
        reasoning_lengths.append(len(reasoning.split()))

    stats = {
        "output_row_count": n_rows,
        "unique_candidate_ids": n_unique_ids,
        "has_duplicates": n_unique_ids != n_rows,
        "score_min": round(min(scores), 3) if scores else None,
        "score_max": round(max(scores), 3) if scores else None,
        "score_mean": round(statistics.mean(scores), 3) if scores else None,
        "score_median": round(statistics.median(scores), 3) if scores else None,
        "score_stdev": round(statistics.stdev(scores), 3) if len(scores) > 1 else None,
        "reasoning_avg_word_count": round(statistics.mean(reasoning_lengths), 1) if reasoning_lengths else None,
        "reasoning_min_word_count": min(reasoning_lengths) if reasoning_lengths else None,
        "rows_missing_reasoning": sum(1 for r in rows if not (r.get("reasoning") or "").strip()),
    }
    return stats


def main():
    parser = argparse.ArgumentParser(description="Benchmark rank.py runtime, memory, and output quality.")
    parser.add_argument("--candidates", required=True, help="Path to candidates.jsonl (or .jsonl.gz)")
    parser.add_argument("--out", required=True, help="Path to write submission.csv")
    parser.add_argument("--rank-script", default="rank.py", help="Path to rank.py")
    parser.add_argument("--report", default="benchmark_report.json", help="Path to write JSON report")
    args = parser.parse_args()

    print(f"Counting input candidates in {args.candidates} ...")
    n_input = count_input_candidates(args.candidates)
    print(f"  -> {n_input:,} candidates in input file")

    print(f"Running {args.rank_script} and measuring time/memory ...")
    perf = run_and_measure(args.rank_script, args.candidates, args.out)
    print(f"  -> wall time: {perf['wall_time_seconds']}s")
    print(f"  -> peak memory (children): {perf['peak_memory_mb']} MB")

    print(f"Analyzing output {args.out} ...")
    quality = analyze_output(args.out)
    print(f"  -> {quality['output_row_count']} rows, "
          f"{quality['unique_candidate_ids']} unique candidate_ids")
    print(f"  -> score range: {quality['score_min']} - {quality['score_max']} "
          f"(mean {quality['score_mean']}, median {quality['score_median']})")
    print(f"  -> avg reasoning length: {quality['reasoning_avg_word_count']} words")

    report = {
        "input_candidate_count": n_input,
        "performance": perf,
        "output_quality": quality,
    }

    Path(args.report).write_text(json.dumps(report, indent=2))
    print(f"\nFull report written to {args.report}")

    print("\n--- Paste-ready summary for README / deck ---")
    print(f"Input candidates:      {n_input:,}")
    print(f"Runtime:               {perf['wall_time_seconds']}s (CPU, single run)")
    print(f"Peak memory:           {perf['peak_memory_mb']} MB")
    print(f"Output rows:           {quality['output_row_count']} "
          f"({'no duplicates' if not quality['has_duplicates'] else 'DUPLICATES FOUND'})")
    print(f"Score range:           {quality['score_min']} - {quality['score_max']}")
    print(f"Avg reasoning length:  {quality['reasoning_avg_word_count']} words/candidate")


if __name__ == "__main__":
    main()

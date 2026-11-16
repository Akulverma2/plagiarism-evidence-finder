"""Comprehensive Performance Benchmarking Suite.

Conducts empirical runtime, comparison count, and memory measurements across:
- Small, medium, and large document sizes (up to 105,000 words)
- Divide & Conquer vs Brute Force baseline
- k-gram sensitivity evaluation
- Exports genuine data to CSV, JSON, and high-res Matplotlib charts
"""

import os
import json
import time
import pandas as pd
from typing import List, Dict, Any

from src.algorithms.divide_and_conquer import run_divide_and_conquer
from src.algorithms.brute_force import run_brute_force
from src.datasets.generator import generate_natural_text, create_plagiarized_pair
from src.visualizer.charts import export_all_plots, plot_k_sensitivity
import matplotlib.pyplot as plt


BENCHMARK_SIZES = [50, 100, 250, 500, 1000, 2000, 5000, 10000, 25000, 50000, 100000]
BRUTE_FORCE_MAX_SIZE = 2500  # Cap BF at 2500 words to maintain feasible test duration


def run_scaling_benchmark(sizes: List[int] = BENCHMARK_SIZES, k: int = 4) -> List[Dict[str, Any]]:
    """Execute scalability benchmark comparing D&C and Brute Force."""
    results: List[Dict[str, Any]] = []

    print(f"Starting Scaling Benchmark across {len(sizes)} sizes (k={k})...")
    for size in sizes:
        print(f"  Benchmarking size: {size} words...")
        base_text = generate_natural_text(size, seed=size + 7)
        src_text, susc_text, _ = create_plagiarized_pair(base_text, 30.0, seed=size + 13)

        # 1. Run Divide and Conquer
        dc_res = run_divide_and_conquer(susc_text, src_text, k=k)

        row = {
            "input_size": size,
            "k": k,
            "dc_time_sec": round(dc_res.execution_time_seconds, 6),
            "dc_comparisons": dc_res.comparison_count,
            "dc_memory_kb": round(dc_res.memory_peak_kb, 2),
            "dc_similarity_pct": dc_res.similarity_percentage,
            "dc_matches": len(dc_res.matches),
            "bf_time_sec": None,
            "bf_comparisons": None,
            "bf_memory_kb": None,
            "bf_similarity_pct": None,
        }

        # 2. Run Brute Force if size <= threshold
        if size <= BRUTE_FORCE_MAX_SIZE:
            bf_res = run_brute_force(susc_text, src_text, k=k)
            row["bf_time_sec"] = round(bf_res.execution_time_seconds, 6)
            row["bf_comparisons"] = bf_res.comparison_count
            row["bf_memory_kb"] = round(bf_res.memory_peak_kb, 2)
            row["bf_similarity_pct"] = bf_res.similarity_percentage
            # Verify parity
            assert dc_res.similarity_percentage == bf_res.similarity_percentage, (
                f"Parity mismatch at size {size}: DC={dc_res.similarity_percentage}%, BF={bf_res.similarity_percentage}%"
            )

        results.append(row)

    return results


def run_k_sensitivity_benchmark(doc_size: int = 2000) -> Dict[str, Any]:
    """Evaluate performance and match discovery across varying k values."""
    k_range = [2, 3, 4, 5, 6, 8, 10, 15, 20]
    base_text = generate_natural_text(doc_size, seed=999)
    src_text, susc_text, _ = create_plagiarized_pair(base_text, 40.0, seed=888)

    runtimes = []
    matches_counts = []

    for k_val in k_range:
        res = run_divide_and_conquer(susc_text, src_text, k=k_val)
        runtimes.append(res.execution_time_seconds)
        matches_counts.append(len(res.matches))

    return {
        "k_values": k_range,
        "runtimes": runtimes,
        "matches_counts": matches_counts
    }


def execute_full_benchmark_suite(output_dir: str = "benchmarks"):
    """Run complete benchmark suite and persist all outputs."""
    os.makedirs(output_dir, exist_ok=True)
    charts_dir = os.path.join("assets", "charts")
    os.makedirs(charts_dir, exist_ok=True)

    # Scaling benchmark
    scaling_data = run_scaling_benchmark()
    df_scaling = pd.DataFrame(scaling_data)
    csv_path = os.path.join(output_dir, "scaling_benchmark.csv")
    df_scaling.to_csv(csv_path, index=False)
    print(f"Scaling data saved to: {csv_path}")

    # Export charts
    export_all_plots(scaling_data, output_dir=charts_dir)
    print(f"Charts saved to: {charts_dir}")

    # k sensitivity benchmark
    k_data = run_k_sensitivity_benchmark()
    k_json_path = os.path.join(output_dir, "k_sensitivity.json")
    with open(k_json_path, "w", encoding="utf-8") as f:
        json.dump(k_data, f, indent=2)

    fig_k = plot_k_sensitivity(k_data["k_values"], k_data["runtimes"], k_data["matches_counts"])
    fig_k.savefig(os.path.join(charts_dir, "k_sensitivity.png"), bbox_inches="tight")
    plt.close(fig_k)
    print("Full benchmark suite completed successfully.")


if __name__ == "__main__":
    execute_full_benchmark_suite()

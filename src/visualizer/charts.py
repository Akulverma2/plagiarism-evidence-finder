"""Professional Matplotlib charts styled for SaaS analytics dashboards.

Design System Alignment:
- Background: #FFFFFF with subtle #F1F5F9 grid
- Divide & Conquer: #5267C5 (Primary Accent)
- Brute Force: #D85B62 (Coral / Danger)
- Word Comparisons: #238B68 (Success Teal)
- Typography: Clean sans-serif with subtle axis styling
"""

import os
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# Modern Linear/Notion dashboard plot aesthetic
plt.rcParams.update({
    "font.sans-serif": ["Inter", "Segoe UI", "DejaVu Sans", "sans-serif"],
    "font.size": 9.5,
    "axes.labelsize": 10.5,
    "axes.titlesize": 11.5,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "figure.titlesize": 12.5,
    "figure.facecolor": "#FFFFFF",
    "axes.facecolor": "#FFFFFF",
    "axes.edgecolor": "#E6E9EF",
    "axes.linewidth": 1.0,
    "grid.color": "#F1F5F9",
    "grid.alpha": 0.9,
    "grid.linestyle": "-",
    "lines.linewidth": 2.2,
    "lines.markersize": 5.5,
})


def plot_runtime_comparison(data: List[Dict[str, Any]], log_scale: bool = True) -> plt.Figure:
    """Plot Execution Time comparison between Divide & Conquer and Brute Force."""
    fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=130)

    sizes = [d["input_size"] for d in data]
    dc_times = [d["dc_time_sec"] for d in data]
    bf_times = [d.get("bf_time_sec") for d in data]

    ax.plot(
        sizes, dc_times,
        marker="o", color="#5267C5",
        label="Divide & Conquer (O(N log N))",
        zorder=4
    )

    valid_bf_pairs = [(s, t) for s, t in zip(sizes, bf_times) if t is not None]
    if valid_bf_pairs:
        bf_s, bf_t = zip(*valid_bf_pairs)
        ax.plot(
            bf_s, bf_t,
            marker="s", color="#D85B62",
            linestyle="--",
            label="Brute Force (O(N · M · k))",
            zorder=3
        )

    ax.set_xlabel("Document Length (Words)", color="#687386", labelpad=8)
    ax.set_ylabel("Execution Time (seconds)", color="#687386", labelpad=8)
    ax.set_title("Runtime Scaling Comparison", color="#172033", pad=12, fontweight="600")
    ax.tick_params(colors="#687386")
    ax.grid(True)

    if log_scale:
        ax.set_xscale("log")
        ax.set_yscale("log")

    legend = ax.legend(
        frameon=True, facecolor="#FFFFFF", edgecolor="#E6E9EF",
        fontsize=9, loc="upper left"
    )
    legend.get_frame().set_boxstyle("square,pad=0.3")

    # Spines
    for spine in ax.spines.values():
        spine.set_color("#E6E9EF")

    fig.tight_layout()
    return fig


def plot_comparison_counts(data: List[Dict[str, Any]]) -> plt.Figure:
    """Plot Word Comparison Count comparison on logarithmic scale."""
    fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=130)

    sizes = [d["input_size"] for d in data]
    dc_comps = [d["dc_comparisons"] for d in data]
    bf_comps = [d.get("bf_comparisons") for d in data]

    ax.plot(
        sizes, dc_comps,
        marker="^", color="#238B68",
        label="Divide & Conquer Operations",
        zorder=4
    )

    valid_bf = [(s, c) for s, c in zip(sizes, bf_comps) if c is not None]
    if valid_bf:
        s_bf, c_bf = zip(*valid_bf)
        ax.plot(
            s_bf, c_bf,
            marker="x", color="#D85B62",
            linestyle=":",
            label="Brute Force Comparisons",
            zorder=3
        )

    ax.set_xlabel("Document Length (Words)", color="#687386", labelpad=8)
    ax.set_ylabel("Word Equality Operations (Log Scale)", color="#687386", labelpad=8)
    ax.set_title("Word Comparison Operations vs Document Size", color="#172033", pad=12, fontweight="600")
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.tick_params(colors="#687386")
    ax.grid(True)

    legend = ax.legend(
        frameon=True, facecolor="#FFFFFF", edgecolor="#E6E9EF",
        fontsize=9, loc="upper left"
    )
    legend.get_frame().set_boxstyle("square,pad=0.3")

    for spine in ax.spines.values():
        spine.set_color("#E6E9EF")

    fig.tight_layout()
    return fig


def plot_k_sensitivity(k_values: List[int], runtimes: List[float], matches_counts: List[int]) -> plt.Figure:
    """Plot impact of varying minimum match length k on runtime and detected matches."""
    fig, ax1 = plt.subplots(figsize=(7.5, 4.2), dpi=130)

    color_time = "#5267C5"
    color_matches = "#D69A36"

    ax1.set_xlabel("Minimum Match Length k (words)", color="#687386", labelpad=8)
    ax1.set_ylabel("Execution Time (ms)", color=color_time, labelpad=8)
    line1 = ax1.plot(
        k_values, [t * 1000 for t in runtimes],
        marker="o", color=color_time,
        label="Runtime (ms)", zorder=4
    )
    ax1.tick_params(axis="y", labelcolor=color_time)
    ax1.tick_params(axis="x", labelcolor="#687386")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Detected Matches Count", color=color_matches, labelpad=8)
    line2 = ax2.plot(
        k_values, matches_counts,
        marker="s", color=color_matches,
        linestyle="--", label="Detected Matches", zorder=3
    )
    ax2.tick_params(axis="y", labelcolor=color_matches)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    legend = ax1.legend(
        lines, labels, loc="upper right",
        frameon=True, facecolor="#FFFFFF", edgecolor="#E6E9EF", fontsize=9
    )
    legend.get_frame().set_boxstyle("square,pad=0.3")

    for spine in ax1.spines.values():
        spine.set_color("#E6E9EF")
    for spine in ax2.spines.values():
        spine.set_color("#E6E9EF")

    plt.title("Parameter Sensitivity: Window Size k Impact", color="#172033", pad=12, fontweight="600")
    fig.tight_layout()
    return fig


def export_all_plots(benchmark_data: List[Dict[str, Any]], output_dir: str = "assets/charts"):
    """Generate and save publication charts to disk."""
    os.makedirs(output_dir, exist_ok=True)

    fig1 = plot_runtime_comparison(benchmark_data, log_scale=True)
    fig1.savefig(os.path.join(output_dir, "runtime_comparison_log.png"), bbox_inches="tight")
    plt.close(fig1)

    fig2 = plot_runtime_comparison(benchmark_data, log_scale=False)
    fig2.savefig(os.path.join(output_dir, "runtime_comparison_linear.png"), bbox_inches="tight")
    plt.close(fig2)

    fig3 = plot_comparison_counts(benchmark_data)
    fig3.savefig(os.path.join(output_dir, "comparison_counts_log.png"), bbox_inches="tight")
    plt.close(fig3)

"""Command-line interface (CLI) for Plagiarism Evidence Finder.

Usage:
    python run_cli.py --suspect path/to/suspect.txt --source path/to/source.txt --k 3 --algo dc
    python run_cli.py --reference
"""

import argparse
import sys
import os
import json

from src.algorithms.divide_and_conquer import run_divide_and_conquer
from src.algorithms.brute_force import run_brute_force
from src.preprocessing.file_reader import read_uploaded_file


def run_analysis(suspect_text: str, source_text: str, k: int, algo: str):
    """Run analysis and format output for terminal display."""
    print("=" * 70)
    print("  UPES DEHRADUN — DAA PROBLEM 17: PLAGIARISM EVIDENCE FINDER")
    print("  Divide & Conquer vs Brute Force Algorithmic Analysis")
    print("=" * 70)

    if algo in ("dc", "both"):
        res_dc = run_divide_and_conquer(suspect_text, source_text, k=k)
        print("\n[DIVIDE & CONQUER RESULTS]")
        print(f"  Similarity Percentage : {res_dc.similarity_percentage:.2f}%")
        print(f"  Copied Word Count     : {res_dc.copied_word_count} / {res_dc.total_suspect_words}")
        print(f"  Total Source Words    : {res_dc.total_source_words}")
        print(f"  Copied Passages Found : {len(res_dc.matches)}")
        print(f"  Word Comparisons      : {res_dc.comparison_count:,}")
        print(f"  Execution Time        : {res_dc.execution_time_seconds:.6f} seconds")
        print(f"  Peak Memory           : {res_dc.memory_peak_kb:.2f} KB")

        print("\n  Evidence Passages:")
        for idx, m in enumerate(res_dc.matches, 1):
            print(f"    Passage #{idx}: \"{m.matched_text}\"")
            print(f"      Suspect Positions : [{m.suspect_start}..{m.suspect_end}] (Length: {m.length} words)")
            print(f"      Source Positions  : [{m.source_start}..{m.source_end}]")

    if algo in ("bf", "both"):
        res_bf = run_brute_force(suspect_text, source_text, k=k)
        print("\n[BRUTE FORCE RESULTS]")
        print(f"  Similarity Percentage : {res_bf.similarity_percentage:.2f}%")
        print(f"  Copied Word Count     : {res_bf.copied_word_count} / {res_bf.total_suspect_words}")
        print(f"  Total Source Words    : {res_bf.total_source_words}")
        print(f"  Copied Passages Found : {len(res_bf.matches)}")
        print(f"  Word Comparisons      : {res_bf.comparison_count:,}")
        print(f"  Execution Time        : {res_bf.execution_time_seconds:.6f} seconds")
        print(f"  Peak Memory           : {res_bf.memory_peak_kb:.2f} KB")

    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Plagiarism Evidence Finder CLI")
    parser.add_argument("--suspect", type=str, help="Path to suspect document or raw text")
    parser.add_argument("--source", type=str, help="Path to source document or raw text")
    parser.add_argument("-k", type=int, default=3, help="Minimum match length (k-gram size, default: 3)")
    parser.add_argument("--algo", choices=["dc", "bf", "both"], default="both", help="Algorithm choice")
    parser.add_argument("--reference", action="store_true", help="Run UPES mandatory reference test")

    args = parser.parse_args()

    if args.reference:
        source_text = "the quick brown fox jumps over the lazy dog near the river bank"
        suspect_text = "yesterday the quick brown fox jumps over a sleeping dog near the river bank today"
        print("Running UPES Reference Test (k=3)...")
        run_analysis(suspect_text, source_text, k=3, algo="both")
        return

    if not args.suspect or not args.source:
        print("Error: Both --suspect and --source are required (or use --reference).")
        parser.print_help()
        sys.exit(1)

    # Read suspect
    if os.path.exists(args.suspect):
        ok, suspect_text, err = read_uploaded_file(args.suspect, args.suspect)
        if not ok:
            print(f"Error reading suspect file: {err}")
            sys.exit(1)
    else:
        suspect_text = args.suspect

    # Read source
    if os.path.exists(args.source):
        ok, source_text, err = read_uploaded_file(args.source, args.source)
        if not ok:
            print(f"Error reading source file: {err}")
            sys.exit(1)
    else:
        source_text = args.source

    run_analysis(suspect_text, source_text, k=args.k, algo=args.algo)


if __name__ == "__main__":
    main()

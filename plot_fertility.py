#!/usr/bin/env python3
"""Plot BPE fertility as a function of vocabulary size."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", type=Path, default=Path("results/fertility_by_vocab.csv"))
    parser.add_argument("--out", type=Path, default=Path("figures/fertility_vs_vocab.png"))
    args = parser.parse_args()

    rows = read_rows(args.metrics)
    bpe = [r for r in rows if r["tokenizer"].startswith("bpe_")]
    bpe = sorted(bpe, key=lambda r: int(r["vocab_size"]))

    xs = [int(r["vocab_size"]) for r in bpe]
    ys = [float(r["fertility"]) for r in bpe]
    char = next((float(r["fertility"]) for r in rows if r["tokenizer"] == "character"), None)
    byte = next((float(r["fertility"]) for r in rows if r["tokenizer"] == "byte_level"), None)

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.plot(xs, ys, marker="o", linewidth=2, label="Russian-trained BPE")
    if char is not None:
        ax.axhline(char, linestyle="--", label=f"character baseline ({char:.2f})")
    if byte is not None:
        ax.axhline(byte, linestyle="--", label=f"English-centric byte-level ({byte:.2f})")

    for x, y in zip(xs, ys):
        ax.text(x, y + 0.06, f"{y:.2f}", ha="center", va="bottom")

    ax.set_xlabel("BPE vocabulary size")
    ax.set_ylabel("Fertility (tokens / word)")
    ax.set_yscale("log")
    ax.grid(True, linestyle=":", linewidth=0.8)
    ax.legend(frameon=True)
    fig.tight_layout()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=300)
    print(f"Saved {args.out}")


if __name__ == "__main__":
    main()

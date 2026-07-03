#!/usr/bin/env python3
"""Export a HuggingFace BPE tokenizer JSON into a small browser-friendly JS file.

The generated file defines:

    window.BPE_MODEL = {vocab: {...}, merges: [[a,b], ...]}

You can import that object in an HTML page and implement deterministic BPE encoding.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tokenizer", type=Path, default=Path("models/bpe_900.json"))
    parser.add_argument("--out", type=Path, default=Path("web_model.js"))
    args = parser.parse_args()

    data = json.loads(args.tokenizer.read_text(encoding="utf-8"))
    model = data.get("model", {})
    vocab = model.get("vocab")
    merges = model.get("merges")

    if vocab is None or merges is None:
        raise ValueError("Could not find BPE vocab/merges in tokenizer JSON.")

    # tokenizers may store merges either as strings "a b" or as lists ["a", "b"]
    normalized_merges = []
    for m in merges:
        if isinstance(m, str):
            parts = m.split()
        else:
            parts = list(m)
        if len(parts) == 2:
            normalized_merges.append(parts)

    out_obj = {"vocab": vocab, "merges": normalized_merges}
    args.out.write_text("window.BPE_MODEL = " + json.dumps(out_obj, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"Saved {args.out}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Evaluate fertility and paradigm type-reuse for trained tokenizers."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Iterable

from tokenizers import Tokenizer

WORD_RE = re.compile(r"[А-Яа-яЁё]+", re.UNICODE)


def words_from_paradigms(paradigms: dict[str, list[str]]) -> list[str]:
    return [form for forms in paradigms.values() for form in forms]


def encode_tokens(tokenizer: Tokenizer, word: str) -> list[str]:
    return tokenizer.encode(word).tokens


def fertility_for_tokenizer(tokenizer: Tokenizer, words: Iterable[str]) -> float:
    words = list(words)
    if not words:
        return 0.0
    return sum(len(encode_tokens(tokenizer, w)) for w in words) / len(words)


def char_fertility(words: Iterable[str]) -> float:
    words = list(words)
    return sum(len(w) for w in words) / len(words)


def byte_fertility(words: Iterable[str]) -> float:
    words = list(words)
    return sum(len(w.encode("utf-8")) for w in words) / len(words)


def paradigm_type_reuse(tokenizer: Tokenizer, paradigms: dict[str, list[str]]) -> list[dict[str, str | int]]:
    rows = []
    for lemma, forms in paradigms.items():
        all_tokens: list[str] = []
        for form in forms:
            all_tokens.extend(encode_tokens(tokenizer, form))
        rows.append({
            "lemma": lemma,
            "forms": len(forms),
            "tokens_total": len(all_tokens),
            "types_unique": len(set(all_tokens)),
        })
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=Path, default=Path("models"))
    parser.add_argument("--paradigms", type=Path, default=Path("data/eval_paradigms.json"))
    parser.add_argument("--out", type=Path, default=Path("results"))
    args = parser.parse_args()

    paradigms = json.loads(args.paradigms.read_text(encoding="utf-8"))
    eval_words = words_from_paradigms(paradigms)

    fertility_rows = [
        {"tokenizer": "character", "vocab_size": "", "fertility": round(char_fertility(eval_words), 4)},
        {"tokenizer": "byte_level", "vocab_size": "", "fertility": round(byte_fertility(eval_words), 4)},
    ]

    reuse_rows = []
    for model_path in sorted(args.models.glob("*.json")):
        tokenizer = Tokenizer.from_file(str(model_path))
        name = model_path.stem
        vocab_size = name.split("_")[-1] if "_" in name else ""
        fertility_rows.append({
            "tokenizer": name,
            "vocab_size": vocab_size,
            "fertility": round(fertility_for_tokenizer(tokenizer, eval_words), 4),
        })
        for row in paradigm_type_reuse(tokenizer, paradigms):
            row = {"tokenizer": name, **row}
            reuse_rows.append(row)

    write_csv(args.out / "fertility_by_vocab.csv", fertility_rows)
    write_csv(args.out / "paradigm_type_reuse.csv", reuse_rows)

    print(f"Saved {args.out / 'fertility_by_vocab.csv'}")
    print(f"Saved {args.out / 'paradigm_type_reuse.csv'}")


if __name__ == "__main__":
    main()

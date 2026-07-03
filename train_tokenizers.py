#!/usr/bin/env python3
"""Train Russian BPE and Unigram tokenizers from scratch."""

from __future__ import annotations

import argparse
from pathlib import Path

from tokenizers import Tokenizer, models, pre_tokenizers, trainers


def train_bpe(corpus: Path, out_dir: Path, vocab_size: int) -> Path:
    tokenizer = Tokenizer(models.BPE(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        min_frequency=1,
        special_tokens=["[UNK]"],
        show_progress=True,
    )
    tokenizer.train([str(corpus)], trainer)
    out_path = out_dir / f"bpe_{vocab_size}.json"
    tokenizer.save(str(out_path))
    return out_path


def train_unigram(corpus: Path, out_dir: Path, vocab_size: int) -> Path:
    tokenizer = Tokenizer(models.Unigram())
    tokenizer.pre_tokenizer = pre_tokenizers.Metaspace(replacement="_", prepend_scheme="always")
    trainer = trainers.UnigramTrainer(
        vocab_size=vocab_size,
        unk_token="[UNK]",
        special_tokens=["[UNK]"],
        show_progress=True,
    )
    tokenizer.train([str(corpus)], trainer)
    out_path = out_dir / f"unigram_{vocab_size}.json"
    tokenizer.save(str(out_path))
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=Path("data/corpus.txt"))
    parser.add_argument("--out", type=Path, default=Path("models"))
    parser.add_argument("--bpe-vocabs", type=int, nargs="+", default=[300, 500, 700, 900, 1200])
    parser.add_argument("--unigram-vocab", type=int, default=900)
    args = parser.parse_args()

    if not args.corpus.exists():
        raise FileNotFoundError(f"Corpus not found: {args.corpus}. Run src/build_corpus.py first.")

    args.out.mkdir(parents=True, exist_ok=True)
    for vocab_size in args.bpe_vocabs:
        path = train_bpe(args.corpus, args.out, vocab_size)
        print(f"Saved {path}")
    path = train_unigram(args.corpus, args.out, args.unigram_vocab)
    print(f"Saved {path}")


if __name__ == "__main__":
    main()

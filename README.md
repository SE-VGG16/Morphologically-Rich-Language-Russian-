# Root, Suffix, or Byte? Tokenizing Russian

This repository contains the code and browser demo for a small reproducible study of subword tokenization for Russian.

The project compares:

- Russian-trained BPE tokenization
- Unigram tokenization
- character-level baseline
- English-centric byte-level fallback

The main idea is to show two effects:

1. **Coverage penalty**: a tokenizer that has not learned Cyrillic spends many more tokens on the same Russian text.
2. **Compression vs. morphology**: low fertility is not always good morphological segmentation. BPE may memorize whole inflected forms, while Unigram can reuse roots across related forms.

## Project structure

```text
russian-tokenizer-project/
├── index.html                         # interactive browser demo, ready for GitHub Pages
├── data/
│   ├── sample_corpus.txt              # small Russian corpus example
│   └── eval_paradigms.json            # held-out lemma paradigms
├── src/
│   ├── build_corpus.py                # generate a morphology-dense Russian corpus
│   ├── train_tokenizers.py            # train BPE and Unigram tokenizers
│   ├── evaluate_tokenizers.py         # fertility + paradigm type-reuse metrics
│   ├── plot_fertility.py              # create fertility-vs-vocab plot
│   └── export_bpe_for_browser.py      # export trained BPE vocab/merges for web use
├── figures/                           # paper-ready visual examples
├── models/                            # trained tokenizer files will be saved here
├── results/                           # CSV outputs will be saved here
├── requirements.txt
├── LICENSE
└── .nojekyll
```

## Quick start

```bash
pip install -r requirements.txt
python src/build_corpus.py --out data/corpus.txt
python src/train_tokenizers.py --corpus data/corpus.txt --out models
python src/evaluate_tokenizers.py --models models --paradigms data/eval_paradigms.json --out results
python src/plot_fertility.py --metrics results/fertility_by_vocab.csv --out figures/fertility_vs_vocab.png
```

## Run the browser demo locally

Open `index.html` directly in a browser, or run:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```


Your public demo link will look like:

```text
https://YOUR_USERNAME.github.io/russian-tokenizer/
```

## Notes

The corpus is intentionally small and partly synthetic. The goal is not to train a production tokenizer, but to make the coverage penalty and morphology/compression trade-off easy to inspect and reproduce.

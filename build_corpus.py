#!/usr/bin/env python3
"""Build a small morphology-dense Russian corpus.

The generated corpus is deliberately compact. It repeats related forms of the
same lemma in varied contexts so tokenizers must decide whether to memorize
whole forms or reuse roots and endings.
"""

from __future__ import annotations

import argparse
from pathlib import Path

NOUN_PARADIGMS = {
    "дом": ["дом", "дома", "дому", "домом", "доме", "домов", "домам", "домами", "домах"],
    "язык": ["язык", "языка", "языку", "языком", "языке", "языки", "языков", "языками"],
    "модель": ["модель", "модели", "моделью", "моделей", "моделям", "моделями"],
    "школа": ["школа", "школы", "школе", "школу", "школой", "школах"],
    "стол": ["стол", "стола", "столу", "столом", "столе", "столов", "столам", "столами", "столах"],
}

ADJECTIVE_PARADIGMS = {
    "большой": ["большой", "большая", "большое", "большие", "большого", "большому", "больших"],
    "новый": ["новый", "новая", "новое", "новые", "нового", "новому", "новых", "новыми"],
    "точный": ["точный", "точная", "точное", "точные", "точного", "точному", "точных", "точными"],
}

VERB_PARADIGMS = {
    "читать": ["читать", "читал", "читаю", "читает", "читала", "читали", "читают", "читавший"],
    "работать": ["работать", "работал", "работаю", "работает", "работала", "работали", "работают", "работавший"],
    "изучать": ["изучать", "изучал", "изучаю", "изучает", "изучала", "изучали", "изучают", "изучавший"],
    "измерять": ["измерять", "измерял", "измеряю", "измеряет", "измеряла", "измеряли", "измеряют", "измерявший"],
}

BASE_SENTENCES = [
    "Русский язык богат формами слов.",
    "Модель разбивает длинные слова на морфемы.",
    "Токенизация должна сохранять корень и окончания.",
    "Байт-уровень без кириллицы тратит слишком много токенов.",
    "Хороший токенизатор учится повторно использовать части слов.",
    "Морфологическая структура помогает обобщать редкие формы.",
]


def generate_lines(repeats: int) -> list[str]:
    lines: list[str] = []
    for _ in range(repeats):
        lines.extend(BASE_SENTENCES)
        for lemma, forms in NOUN_PARADIGMS.items():
            lines.append(f"Лемма {lemma} имеет формы: " + ", ".join(forms) + ".")
            lines.append(" ".join(f"В тексте встречается {form}." for form in forms))
        for lemma, forms in ADJECTIVE_PARADIGMS.items():
            lines.append(f"Прилагательное {lemma} меняет окончания: " + ", ".join(forms) + ".")
        for lemma, forms in VERB_PARADIGMS.items():
            lines.append(f"Глагол {lemma} появляется в формах: " + ", ".join(forms) + ".")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/corpus.txt"))
    parser.add_argument("--repeats", type=int, default=12)
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    lines = generate_lines(args.repeats)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    words = " ".join(lines).split()
    chars = sum(len(w) for w in words)
    print(f"Wrote {args.out}")
    print(f"Running words: {len(words):,}")
    print(f"Characters excluding spaces: {chars:,}")


if __name__ == "__main__":
    main()

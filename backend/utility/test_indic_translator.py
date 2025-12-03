import sys
from argparse import ArgumentParser
from pathlib import Path

from services.indic_trans2 import IndicTranslator, LANGUAGE_CODES


def translate_multiline_text(text: str, src_lang: str, tgt_lang: str, direction: str = "en-indic") -> str:
    """
    Translate a multiline string using IndicTranslator.

    Non-empty lines are translated; empty/whitespace-only lines are preserved.
    """
    translator = IndicTranslator(direction=direction)

    original_lines = text.splitlines()
    non_empty_lines = [line for line in original_lines if line.strip()]

    if not non_empty_lines:
        return ""

    translated_non_empty = translator.translate(
        sentences=non_empty_lines,
        src_lang=src_lang,
        tgt_lang=tgt_lang,
    )

    # Ensure we always have a list to iterate over
    if isinstance(translated_non_empty, str):
        translated_non_empty = [translated_non_empty]

    translated_iter = iter(translated_non_empty)
    output_lines = []

    for line in original_lines:
        if line.strip():
            output_lines.append(next(translated_iter))
        else:
            output_lines.append("")

    return "\n".join(output_lines)


def _build_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Test IndicTranslator on multiline input.")
    parser.add_argument(
        "--src",
        default="eng_Latn",
        help="Source language code (default: eng_Latn).",
    )
    parser.add_argument(
        "--tgt",
        required=True,
        help="Target language code, e.g. hin_Deva, mar_Deva.",
    )
    parser.add_argument(
        "--direction",
        default="en-indic",
        choices=["en-indic", "indic-en", "indic-indic"],
        help="Translation direction (default: en-indic).",
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Optional path to a text file with multiline input. "
        "If omitted, reads from standard input.",
    )
    parser.add_argument(
        "--list-langs",
        action="store_true",
        help="List supported language names and codes and exit.",
    )
    return parser


def main(argv=None) -> None:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.list_langs:
        print("Supported languages:")
        for name, code in LANGUAGE_CODES.items():
            print(f"  {name:10s} -> {code}")
        return

    if args.file:
        text = args.file.read_text(encoding="utf-8")
    else:
        print(
            "Enter/paste multiline text, then press Ctrl+Z and Enter (Windows)\n"
            "or Ctrl+D (Unix) to finish:\n"
        )
        text = sys.stdin.read()

    translated = translate_multiline_text(
        text=text,
        src_lang=args.src,
        tgt_lang=args.tgt,
        direction=args.direction,
    )

    print("\n=== Translated Text ===\n")
    print(translated)


if __name__ == "__main__":
    main()


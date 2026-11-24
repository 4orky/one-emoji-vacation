#!/usr/bin/env python3
"""One Emoji, One Dream Vacation.

Writes exactly one emoji to /output/entry.txt: Mount Fuji (U+1F5FB).

Why this emoji: the judge is a travel editor collecting wordless
postcards and picks the emoji that most makes a stranger want to book
the trip. A snow-capped Fuji is a postcard at a glance, names one
particular dream (Japan, the mountain itself) instead of any generic
holiday, and is the fresh pick against the flood of beaches everyone
else will send -- a mountain where a beach was expected. It is a
single code point, instantly readable at small size on any screen,
and needs no explaining.

The gate the sealed scorer applies: /output/entry.txt must be UTF-8
text of 1 to 8 characters, not only white space. This program
verifies its own output against that gate (plus a single-emoji check)
after writing, and fails loudly instead of shipping a bad file.
"""

import os
import sys
import unicodedata

ENTRY = "\U0001F5FB"  # 🗻 MOUNT FUJI
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/entry.txt")


def is_single_emoji(text: str) -> bool:
    """True when text is exactly one emoji code point.

    U+1F5FB is category So (Symbol, other) with emoji presentation.
    A variation selector or ZWJ sequence would make len(text) > 1,
    so a length-1 So character is exactly one plain emoji.
    """
    return (
        len(text) == 1
        and unicodedata.category(text) == "So"
        and text.isprintable()
    )


def validate(path: str) -> str:
    """Read the written file back and check it against the gate."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not (1 <= len(text) <= 8):
        raise SystemExit(f"gate fail: {len(text)} characters, need 1-8")
    if not text.strip():
        raise SystemExit("gate fail: entry is only white space")
    if not is_single_emoji(text):
        raise SystemExit(f"gate fail: not exactly one emoji: {text!r}")
    return text


def main() -> None:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    text = validate(OUTPUT_PATH)
    print(f"wrote {text!r} ({len(text)} char, "
          f"{len(text.encode('utf-8'))} bytes) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

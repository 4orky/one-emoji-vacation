#!/usr/bin/env python3
"""Dream-vacation postcard: one emoji, nothing else.

The brief asks for a single emoji that stands in for a dream trip,
judged by a travel editor who collects wordless postcards. This
program settles on Mount Fuji -- the snow-capped peak you recognise
from a train window before you can name the country. One picture,
one place, one dream: Japan, the mountain itself, the climb at
dawn. Beaches will flood the field; a mountain where a beach was
expected is the postcard that gets picked up twice.

What the program does: it writes that one emoji to the entry file
(/output/entry.txt by default, overridable with ENTRY_PATH), then
reads the file back and proves, byte by byte, that it holds exactly
that emoji and nothing else. Any mismatch aborts loudly instead of
letting a bad entry through."""

from os import environ
from pathlib import Path
from sys import exit as sys_exit
from unicodedata import category as char_category, name as char_name

# The sealed gate the brief publishes: 1 to 8 characters, not only
# white space. The identity checks below sit on top of that gate.
GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 8

# The chosen postcard: MOUNT FUJI, a single code point U+1F5FB.
FUJI = "\U0001F5FB"
FUJI_UTF8 = b"\xf0\x9f\x97\xbb"
ENTRY_PATH = Path(environ.get("ENTRY_PATH", "/output/entry.txt"))


def describe(ch: str) -> str:
    """One-line human-readable identity of the chosen character."""
    try:
        name = char_name(ch)
    except ValueError:
        name = "UNNAMED"
    return f"U+{ord(ch):04X} {name}"


def check_postcard(path: Path) -> str:
    """Read the entry back and insist it is exactly the chosen emoji.

    Checks run in the same order the brief's gate states them: the
    size gate first, then identity, then the character's own kind.
    """
    raw = path.read_bytes()
    if raw != FUJI_UTF8:
        raise SystemExit(f"entry bytes are not the Fuji postcard: {raw!r}")
    entry = raw.decode("utf-8")
    if not GATE_MIN_CHARS <= len(entry) <= GATE_MAX_CHARS:
        raise SystemExit(
            f"gate fail: {len(entry)} characters, need "
            f"{GATE_MIN_CHARS}-{GATE_MAX_CHARS}"
        )
    if entry.strip() == "":
        raise SystemExit("gate fail: entry holds only white space")
    if entry != FUJI:
        raise SystemExit(f"entry is {entry!r}, need the Fuji emoji")
    if char_category(entry) != "So":
        raise SystemExit(f"entry {entry!r} is not a symbol character")
    return entry


def main() -> int:
    ENTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENTRY_PATH.write_bytes(FUJI_UTF8)
    picked = check_postcard(ENTRY_PATH)
    print(f"postcard written: {picked} ({describe(picked)}) -> {ENTRY_PATH}")
    return 0


if __name__ == "__main__":
    sys_exit(main())

#!/usr/bin/env python3
"""
main.py

Convert lines like:
  https://site.com -> user:pass
  site.com -> user:pass
into:
  https://site.com/wp-login.php#user@pass
  site.com/wp-login.php#user@pass

Usage:
  python3 main.py input.txt > output.txt
  python3 main.py -i input.txt -o out.txt
  cat input.txt | python3 main.py
"""

import argparse
import sys
from typing import Iterable

def normalize_site(site: str) -> str:
    s = site.strip()
    # remove trailing slash(es)
    while s.endswith('/'):
        s = s[:-1]
    return s

def convert_line(line: str, separator: str = '->') -> str | None:
    """Convert a single line, or return None if the line should be ignored."""
    raw = line.strip()
    if not raw:
        return None
    if raw.startswith('#'):
        return None

    # Attempt to split left and right by separator
    if separator in raw:
        left, right = raw.split(separator, 1)
    else:
        # If separator missing, try splitting by whitespace (last token is creds)
        parts = raw.split()
        if len(parts) < 2:
            return None
        left = ' '.join(parts[:-1])
        right = parts[-1]

    left = normalize_site(left)
    right = right.strip()

    # Normalize credentials: user:pass -> user@pass (only first colon separates)
    if ':' in right:
        user, pwd = right.split(':', 1)
    elif '@' in right and ':' not in right:
        # if already user@pass, keep it but don't double replace
        user, pwd = right.split('@', 1)
        right = f"{user}@{pwd}"
        return f"{left}/wp-login.php#{right}"
    else:
        # only user provided (no password)
        user, pwd = right, ''

    creds = f"{user}@{pwd}" if pwd != '' else f"{user}@"

    return f"{left}/wp-login.php#{creds}"

def process_lines(lines: Iterable[str], separator: str = '->') -> list[str]:
    out = []
    for ln in lines:
        conv = convert_line(ln, separator=separator)
        if conv:
            out.append(conv)
    return out

def main():
    parser = argparse.ArgumentParser(description="Convert site -> user:pass into site/wp-login.php#user@pass")
    parser.add_argument('-i', '--input', help='Input file (default: stdin)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('-s', '--separator', default='->', help="Separator between site and creds (default: '->')")
    args = parser.parse_args()

    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                input_lines = f.readlines()
        except Exception as e:
            print(f"Error opening input file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        input_lines = sys.stdin.read().splitlines()

    converted = process_lines(input_lines, separator=args.separator)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                for c in converted:
                    f.write(c + '\n')
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        for c in converted:
            print(c)

if __name__ == "__main__":
    main()

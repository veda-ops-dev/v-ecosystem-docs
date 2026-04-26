#!/usr/bin/env python3
"""
vcheck — VedaOps text artifact integrity checker

Checks markdown files for corruption that is invisible to human review
but breaks automated parsing, linking, auditing, and string matching.

Motivated by a real failure: write tooling injected ESC characters (0x1B)
immediately before backtick-wrapped file references in three doctrine files.
The corruption was undetectable by eye but broke every automated reference
resolution that depended on those paths.

Usage:
  python tools/vcheck.py --guard <file>       check one file, block on failure
  python tools/vcheck.py --sweep [files...]   check one or more files
  python tools/vcheck.py --sweep              sweep all *.md files under cwd

Exit codes:
  0   all files clean
  1   one or more blocking failures
  2   warnings only (no blocking failures)

No external dependencies. Python 3.8+.
"""

import sys
import os
import re
import glob
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Rule definitions
# ---------------------------------------------------------------------------

# Forbidden byte values: control chars except HT (0x09), LF (0x0A), CR (0x0D)
FORBIDDEN_CONTROL = set(range(0x00, 0x20)) - {0x09, 0x0A, 0x0D}
FORBIDDEN_CONTROL.add(0x7F)  # DEL

# Backtick-wrapped .md file reference: e.g. `some-doc.md` or `../path/doc.md`
MD_REF_PATTERN = re.compile(r'`([a-zA-Z0-9_./-]+\.md)`')

# Trailing invisible whitespace on a line (space or tab before newline)
TRAILING_WS_PATTERN = re.compile(r'[ \t]+\r?$', re.MULTILINE)


# ---------------------------------------------------------------------------
# Core checker
# ---------------------------------------------------------------------------

def check_file(path: Path, repo_root: Path) -> tuple[list[str], list[str]]:
    """
    Returns (blocking_errors, warnings).
    Both are lists of human-readable message strings.
    """
    errors: list[str] = []
    warnings: list[str] = []

    # -- Rule: UTF-8 validity ------------------------------------------------
    try:
        raw = path.read_bytes()
        text = raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        errors.append(
            f"ENCODING  not valid UTF-8 at byte offset {exc.start}: {exc.reason}"
        )
        return errors, warnings  # cannot proceed without valid text

    lines = text.splitlines(keepends=True)

    # -- Rules: control character scan (per character, per line) -------------
    for lineno, line in enumerate(lines, 1):
        for col, ch in enumerate(line, 1):
            code = ord(ch)
            if code not in FORBIDDEN_CONTROL:
                continue

            # Check whether this control char sits immediately before a backtick
            # (the exact injection pattern that caused the real failure)
            remainder = line[col - 1:]
            if len(remainder) > 1 and remainder[1] == '`':
                errors.append(
                    f"CTRL_BEFORE_REF  L{lineno}:{col}  "
                    f"U+{code:04X} immediately precedes a backtick — "
                    f"likely tool injection. "
                    f"Context: {repr(line.rstrip())}"
                )
            elif code == 0x00:
                errors.append(
                    f"NULL_BYTE  L{lineno}:{col}  "
                    f"null byte detected — possible binary corruption"
                )
            else:
                errors.append(
                    f"CTRL_CHAR  L{lineno}:{col}  "
                    f"U+{code:04X} in text. "
                    f"Context: {repr(line.rstrip())}"
                )

    # -- Rule: broken backtick .md references (warn only) --------------------
    for lineno, line in enumerate(lines, 1):
        for match in MD_REF_PATTERN.finditer(line):
            ref = match.group(1)
            # Resolve relative to the file's own directory first,
            # then fall back to repo root
            if not (path.parent / ref).exists() and not (repo_root / ref).exists():
                warnings.append(
                    f"BROKEN_REF  L{lineno}  `{ref}` not found "
                    f"(checked relative to file and repo root)"
                )

    # -- Rule: mixed line endings (warn only) --------------------------------
    has_crlf = '\r\n' in text
    # LF that is NOT preceded by CR
    has_bare_lf = bool(re.search(r'(?<!\r)\n', text))
    if has_crlf and has_bare_lf:
        warnings.append(
            "MIXED_ENDINGS  file contains both CRLF and bare LF line endings"
        )

    # -- Rule: trailing invisible whitespace (warn only) ---------------------
    tw_matches = TRAILING_WS_PATTERN.findall(text)
    if tw_matches:
        warnings.append(
            f"TRAILING_WS  {len(tw_matches)} line(s) have trailing "
            f"space or tab before newline"
        )

    return errors, warnings


# ---------------------------------------------------------------------------
# Repo root detection
# ---------------------------------------------------------------------------

def find_repo_root(start: Path) -> Path:
    """Walk up from start to find the .git directory; fall back to cwd."""
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / '.git').exists():
            return candidate
    return Path.cwd()


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run(paths: list[Path]) -> int:
    """
    Check all paths. Returns exit code:
      0  all clean
      1  one or more blocking errors
      2  warnings only
    """
    if not paths:
        # Default sweep: all *.md files under cwd
        paths = [Path(p) for p in sorted(glob.glob('**/*.md', recursive=True))]

    if not paths:
        print("vcheck: no markdown files found.")
        return 0

    repo_root = find_repo_root(paths[0])

    total_errors = 0
    total_warnings = 0
    files_checked = 0

    for path in paths:
        if not path.exists():
            print(f"vcheck: not found: {path}", file=sys.stderr)
            total_errors += 1
            continue

        errors, warnings = check_file(path, repo_root)
        files_checked += 1
        total_errors += len(errors)
        total_warnings += len(warnings)

        if errors or warnings:
            status = "FAIL" if errors else "WARN"
            print(f"\n{status}  {path}")
            for msg in errors:
                print(f"  ERROR  {msg}")
            for msg in warnings:
                print(f"  warn   {msg}")

    # Summary line
    print(
        f"\nvcheck: {files_checked} file(s) checked — "
        f"{total_errors} error(s), {total_warnings} warning(s)."
    )

    if total_errors > 0:
        return 1
    if total_warnings > 0:
        return 2
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="VedaOps text artifact integrity checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--guard',
        metavar='FILE',
        type=Path,
        help='Check a single file and exit non-zero on any blocking failure.',
    )
    group.add_argument(
        '--sweep',
        metavar='FILE',
        nargs='*',
        type=Path,
        help=(
            'Check one or more files. '
            'If no files are given, sweeps all *.md files under cwd.'
        ),
    )
    args = parser.parse_args()

    if args.guard is not None:
        sys.exit(run([args.guard]))
    else:
        sys.exit(run(args.sweep or []))


if __name__ == '__main__':
    main()

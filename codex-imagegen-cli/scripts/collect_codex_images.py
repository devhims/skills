#!/usr/bin/env python3
"""Copy the PNG(s) a `codex exec` image run produced into a project folder.

You run codex yourself (see SKILL.md) and tee its output to a log; this script
reads that log, finds the images, and copies them.

usage: collect_codex_images.py --log RUN.log --out DIR [--name STEM]
Prints one copied PNG path per line. Exit 1 if no image was found.
"""
import argparse
import os
import re
import shutil
import sys
from pathlib import Path

GEN = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex').expanduser() / 'generated_images'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--log', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--name', default='image')
    a = ap.parse_args()
    log_path = Path(a.log).expanduser().resolve()
    log = log_path.read_text(errors='replace')
    out = Path(a.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    found = []
    m = re.search(r'session id:\s*([0-9a-f-]{36})', log)
    if m and (GEN / m.group(1)).is_dir():
        found = sorted((GEN / m.group(1)).glob('*.png'), key=lambda f: f.stat().st_mtime)
    if not found:  # fall back to PNG paths printed in the reply
        for x in dict.fromkeys(re.findall(r'(/[^\s)\]`]+\.png)', log)):
            if Path(x).is_file() and GEN in Path(x).parents:
                found.append(Path(x))
    if not found:
        sys.exit(f'no generated image found for {log_path}; check the log for errors')

    # Codex often checks its own output and generates again (wrong aspect,
    # stray element). The image it settled on is the last generated PNG named
    # in the log, or the newest one when its reply names none.
    named = [p for p in re.findall(r'(/[^\s)\]`]+\.png)', log) if str(GEN) in p]
    final = Path(named[-1]) if named else found[-1]

    for i, f in enumerate(found):
        dst = out / (f'{a.name}.png' if len(found) == 1 else f'{a.name}-{i + 1}.png')
        shutil.copy2(f, dst)
        print(dst)
        if len(found) > 1 and f.name == final.name:
            print(f'final: {dst}', file=sys.stderr)


if __name__ == '__main__':
    main()

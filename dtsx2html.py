#!/usr/bin/env python3
"""Bake one or more SSIS .dtsx packages into a single, self-contained HTML file.

The output is viewer.html with the packages embedded, so it can be opened by
double-clicking or shared without needing the original .dtsx files.

Examples:
    ./dtsx2html.py MyPackage.dtsx                 # -> MyPackage.html
    ./dtsx2html.py path/to/project/ -o all.html   # every .dtsx in a folder
    ./dtsx2html.py a.dtsx b.dtsx --open           # write, then open in browser
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

VIEWER = Path(__file__).resolve().parent / "viewer.html"
PLACEHOLDER = re.compile(
    r'(<script type="application/json" id="embedded-packages">)(.*?)(</script>)', re.S
)


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16")
    return raw.decode("utf-8-sig", errors="replace")


def collect(inputs):
    files = []
    for item in inputs:
        p = Path(item).expanduser()
        if p.is_dir():
            files.extend(sorted(p.rglob("*.dtsx")))
        elif p.is_file():
            files.append(p)
        else:
            sys.exit(f"error: {item} not found")
    if not files:
        sys.exit("error: no .dtsx files found")
    return files


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help=".dtsx files and/or folders containing them")
    ap.add_argument("-o", "--output", help="output HTML path (default: <package>.html or ssis-packages.html)")
    ap.add_argument("--open", action="store_true", help="open the result in the default browser")
    args = ap.parse_args()

    files = collect(args.inputs)
    payload = [{"name": f.name, "text": read_text(f)} for f in files]

    viewer = VIEWER.read_text(encoding="utf-8")
    if not PLACEHOLDER.search(viewer):
        sys.exit(f"error: embed placeholder not found in {VIEWER}")
    # Escape "</" so package content can never close the <script> block early.
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    html = PLACEHOLDER.sub(lambda m: m.group(1) + data + m.group(3), viewer, count=1)

    out = Path(args.output) if args.output else (
        files[0].with_suffix(".html") if len(files) == 1 else Path.cwd() / "ssis-packages.html"
    )
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out} ({len(files)} package{'s' if len(files) != 1 else ''})")
    if args.open:
        subprocess.run(["open", str(out)], check=False)


if __name__ == "__main__":
    main()

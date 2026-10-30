"""Prepare a draw.io SVG for embedding in Word without changing its drawing.

Usage: python prepare_drawio_svg.py exported.svg word-ready.svg
The original SVG is never overwritten.
"""

import argparse
from pathlib import Path
from xml.etree import ElementTree


def prepare(source: Path, target: Path) -> bool:
    if source.resolve() == target.resolve():
        raise ValueError("Input and output paths must differ")
    svg = source.read_text(encoding="utf-8-sig")
    if "<svg" not in svg:
        raise ValueError("Input is not an SVG document")

    marker = "Text is not SVG - cannot display"
    changed = False
    if marker in svg:
        if svg.count(marker) != 1:
            raise ValueError("Unexpected number of draw.io warning overlays")
        start = svg.rfind("<switch>", 0, svg.index(marker))
        end = svg.find("</switch>", svg.index(marker)) + len("</switch>")
        if (start < 0 or end <= start or
                "drawio.com/doc/faq/svg-export-text-problems" not in svg[start:end] or
                svg[end:].strip() != "</svg>"):
            raise ValueError("Warning overlay did not match the known draw.io pattern")
        svg = svg[:start] + svg[end:]
        changed = True

    ElementTree.fromstring(svg)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(svg, encoding="utf-8")
    return changed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    print("warning removed" if prepare(args.source, args.target) else "copied without change")

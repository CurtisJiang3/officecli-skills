"""Match draw.io SVG text and colors to a monochrome Word document.

Run after prepare_drawio_svg.py. Preserve the original .drawio and export SVG.
Example:
  python style_drawio_svg.py clean.svg word.svg --word-width-cm 15 --font-pt 12
"""

import argparse
import re
from pathlib import Path
from xml.etree import ElementTree as ET


SVG = "http://www.w3.org/2000/svg"
XHTML = "http://www.w3.org/1999/xhtml"
XML = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
ET.register_namespace("xhtml", XHTML)


def is_latin(character: str) -> bool:
    return character.isascii() and (character.isalnum() or character in ".-+/_")


def segments(value: str):
    if not value:
        return
    start = 0
    current = is_latin(value[0])
    for index, character in enumerate(value[1:], 1):
        flag = is_latin(character)
        if flag != current:
            yield value[start:index], current
            start, current = index, flag
    yield value[start:], current


def style_svg(source: Path, target: Path, word_width_cm: float, font_pt: float):
    if source.resolve() == target.resolve():
        raise ValueError("Input and output paths must differ")
    if word_width_cm <= 0 or font_pt <= 0:
        raise ValueError("Word width and font size must be positive")

    tree = ET.parse(source)
    root = tree.getroot()
    if root.tag != f"{{{SVG}}}svg":
        raise ValueError("Input is not an SVG document")
    view_box = root.get("viewBox", "").split()
    if len(view_box) != 4:
        raise ValueError("SVG viewBox is required for print-size font matching")
    view_width = float(view_box[2])
    word_width_pt = word_width_cm / 2.54 * 72
    svg_font_px = font_pt * view_width / word_width_pt

    # SVG/CSS background is ignored by some Office previews and dark-mode image
    # viewers. A real painted rectangle keeps black connectors visible everywhere.
    root.set("style", "background:#ffffff")
    view_x, view_y, view_width, view_height = map(float, view_box)
    for element in list(root):
        if element.get("data-word-background") == "true":
            root.remove(element)
    background = ET.Element(f"{{{SVG}}}rect")
    background.set("x", f"{view_x:g}")
    background.set("y", f"{view_y:g}")
    background.set("width", f"{view_width:g}")
    background.set("height", f"{view_height:g}")
    background.set("fill", "#ffffff")
    background.set("data-word-background", "true")
    root.insert(1 if len(root) and root[0].tag == f"{{{SVG}}}defs" else 0, background)
    changed_text = 0
    for element in root.iter():
        if element.tag.startswith(f"{{{SVG}}}") and "light-dark" in element.get("style", ""):
            element.attrib.pop("style", None)
        if element.tag == f"{{{XHTML}}}div":
            style = element.get("style", "")
            if "font-family:" in style:
                style = re.sub(r"font-size:\s*[\d.]+px", f"font-size: {svg_font_px:.2f}px", style)
                style = re.sub(r"font-family:\s*[^;]+", "font-family: 宋体", style)
                style = re.sub(r"color:\s*light-dark\([^;]+\)", "color: #000000", style)
                element.set("style", style)
                original = element.text or ""
                if original:
                    element.text = None
                    for content, latin in segments(original):
                        span = ET.SubElement(element, f"{{{XHTML}}}span")
                        span.set("style", f"font-family: {'Times New Roman' if latin else '宋体'}")
                        span.text = content
                    changed_text += 1
        if element.tag != f"{{{SVG}}}text":
            continue
        original = element.text or ""
        if not original:
            continue
        element.set("fill", "#000000")
        element.set("font-family", "宋体")
        element.set("font-size", f"{svg_font_px:.2f}px")
        element.set(f"{{{XML}}}space", "preserve")
        element.text = None
        for content, latin in segments(original):
            span = ET.SubElement(element, f"{{{SVG}}}tspan")
            span.set("font-family", "Times New Roman" if latin else "宋体")
            span.text = content
        changed_text += 1

    target.parent.mkdir(parents=True, exist_ok=True)
    tree.write(target, encoding="utf-8", xml_declaration=True)
    return changed_text, svg_font_px


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--word-width-cm", type=float, required=True)
    parser.add_argument("--font-pt", type=float, required=True)
    args = parser.parse_args()
    count, px = style_svg(args.source, args.target, args.word_width_cm, args.font_pt)
    print(f"styled {count} text elements; SVG font {px:.2f}px")

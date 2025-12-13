#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract images from a .docx and insert them into markdown files at matching captions.

Strategy:
1) Parse DOCX XML for image references (a:blip r:embed) and nearby captions like "Рис. 1.12."
2) Save images into public/images/milovanov/ as ris_1_12.<ext>
3) Insert markdown image links above matching caption lines in:
   - public/content/chapters/*.md
   - src/content/chapters/*.md

Idempotent: won't insert duplicate image links if already present nearby.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from docx import Document
from docx.oxml.ns import nsmap


DOCX_PATH = Path("public/milovanov-t.docx")
OUT_DIR = Path("public/images/milovanov")
MD_DIRS = [
    Path("public/content/chapters"),
    Path("src/content/chapters"),
]


NS = nsmap  # python-docx namespace map used by BaseOxmlElement.xpath()


CAPTION_RE = re.compile(r"^\s*Рис\.\s*(\d+)\.(\d+)\.?\s*(.*)\s*$", re.IGNORECASE)


@dataclass(frozen=True)
class FigureInfo:
    num: str  # e.g. "1.12"
    title: str  # caption title part (may be empty)
    rel_id: str  # relationship id like "rId7"


def _p_text(p_elm) -> str:
    # collect all text nodes
    ts = p_elm.xpath(".//w:t")
    return "".join(t.text or "" for t in ts).strip()


def _p_embeds(p_elm) -> List[str]:
    return p_elm.xpath(".//a:blip/@r:embed")


def extract_figures_from_docx(doc: Document) -> Dict[str, FigureInfo]:
    """
    Returns mapping: figure_number -> FigureInfo.
    """
    figures: Dict[str, FigureInfo] = {}

    # Traverse all paragraphs in body, including those inside tables, in document order.
    body = doc.element.body
    p_elms = body.xpath(".//w:p")

    last_embed: Optional[str] = None

    for p in p_elms:
        embeds = _p_embeds(p)
        text = _p_text(p)

        # If this paragraph has an image, remember the last one (common: image paragraph then caption paragraph)
        if embeds:
            last_embed = embeds[-1]

        m = CAPTION_RE.match(text)
        if not m:
            continue

        fig_num = f"{m.group(1)}.{m.group(2)}"
        fig_title = (m.group(3) or "").strip()

        # Prefer embed in same paragraph if present; else fallback to last seen embed.
        rel_id = embeds[-1] if embeds else last_embed
        if not rel_id:
            continue

        # Keep first occurrence (some docs repeat captions in TOC)
        if fig_num not in figures:
            figures[fig_num] = FigureInfo(num=fig_num, title=fig_title, rel_id=rel_id)

    return figures


def save_images(doc: Document, figures: Dict[str, FigureInfo]) -> Dict[str, Path]:
    """
    Saves images for each figure and returns mapping figure_number -> saved path (relative to public).
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    out_map: Dict[str, Path] = {}

    for fig_num, info in sorted(figures.items(), key=lambda kv: tuple(int(x) for x in kv[0].split("."))):
        rel = doc.part.rels.get(info.rel_id)
        if not rel:
            continue

        part = rel.target_part
        # part.partname like '/word/media/image1.png'
        name = str(part.partname).split("/")[-1]
        ext = name.split(".")[-1].lower() if "." in name else "png"

        safe_num = fig_num.replace(".", "_")
        out_name = f"ris_{safe_num}.{ext}"
        out_path = OUT_DIR / out_name

        out_path.write_bytes(part.blob)
        out_map[fig_num] = out_path

    return out_map


def md_image_line(fig_num: str, img_web_path: str, caption_title: str) -> str:
    alt = f"Рис. {fig_num}"
    if caption_title:
        alt = f"{alt}. {caption_title}"
    return f"![{alt}]({img_web_path})"


def insert_into_md(md_path: Path, fig_num: str, img_web_path: str, caption_title: str) -> bool:
    """
    Insert image markdown line above the caption line containing 'Рис. {fig_num}'.
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Skip if this image already referenced anywhere
    if img_web_path in text:
        return False

    caption_pat = re.compile(rf"^\s*(\*\*)?Рис\.\s*{re.escape(fig_num)}\b", re.IGNORECASE)

    changed = False
    out: List[str] = []
    inserted = False

    for i, line in enumerate(lines):
        if not inserted and caption_pat.search(line):
            # Avoid inserting if previous lines already have an image line
            prev_window = "\n".join(lines[max(0, i - 3) : i])
            if "![" not in prev_window:
                out.append(md_image_line(fig_num, img_web_path, caption_title))
                out.append("")  # blank line for markdown readability
                inserted = True
                changed = True
        out.append(line)

    if changed:
        md_path.write_text("\n".join(out) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    return changed


def main() -> None:
    if not DOCX_PATH.exists():
        raise SystemExit(f"DOCX not found: {DOCX_PATH}")

    doc = Document(str(DOCX_PATH))
    figures = extract_figures_from_docx(doc)
    if not figures:
        print("No figures found (captions like 'Рис. X.Y').")
        return

    img_map = save_images(doc, figures)
    print(f"Extracted images: {len(img_map)} into {OUT_DIR.as_posix()}")

    total_inserted = 0
    for md_dir in MD_DIRS:
        if not md_dir.exists():
            continue
        md_files = list(md_dir.glob("*.md"))
        inserted_here = 0
        for fig_num, info in figures.items():
            out_path = img_map.get(fig_num)
            if not out_path:
                continue
            img_web_path = "/" + out_path.as_posix().replace("public/", "")
            for md in md_files:
                if insert_into_md(md, fig_num, img_web_path, info.title):
                    inserted_here += 1
        print(f"Inserted into {md_dir.as_posix()}: {inserted_here} changes")
        total_inserted += inserted_here

    print(f"Done. Total markdown edits: {total_inserted}")


if __name__ == "__main__":
    main()



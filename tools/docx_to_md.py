#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert public/milovanov-t.docx into Markdown chapters/sections as used by the app.

Goals:
- Follow DOCX structure (Heading 2/3/4...) to build chapters and sections.
- Preserve paragraphs and inline emphasis (bold/italic) as much as possible.
- Preserve Word lists (numbering/bullets) via numbering.xml mapping.
- Convert tables to GitHub-flavored Markdown tables (remark-gfm is enabled in the app).
- Keep figure captions like "Рис. 1.17. ..." verbatim so tools/extract_docx_images_and_insert.py
  can insert the extracted images at correct locations.
- Write BOTH:
  - public/content/chapters/*.md (runtime content)
  - src/content/chapters/*.md (source mirror)
  and update src/data/chapters.ts accordingly.

This script intentionally wipes stale markdown files in the target dirs that are not generated.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph


DOCX_PATH = Path("public/milovanov-t.docx")
OUT_PUBLIC_DIR = Path("public/content/chapters")
OUT_SRC_DIR = Path("src/content/chapters")
CHAPTERS_TS = Path("src/data/chapters.ts")


HEADING_RE = re.compile(r"^\s*(\d+)\.\s*(.+?)\s*$")
TOC_TITLE_RE = re.compile(r"^\s*СОДЕРЖАНИЕ\s*$", re.IGNORECASE)


def slugify_ru(text: str) -> str:
    t = (text or "").strip().lower()
    t = re.sub(r"[«»\"“”]", "", t)
    t = t.replace("—", "-").replace("–", "-")
    t = re.sub(r"\s+", "-", t)
    # keep cyrillic + latin + digits + dash
    t = re.sub(r"[^0-9a-zа-яё\-]+", "", t, flags=re.IGNORECASE)
    t = re.sub(r"-{2,}", "-", t).strip("-")
    return t or "section"


def norm_spaces(s: str) -> str:
    # Keep readability, but don't smash meaningful spacing in formulas too aggressively.
    s = s.replace("\t", " ")
    s = re.sub(r"[ \u00A0]{2,}", " ", s)
    return s


def escape_md_text(s: str) -> str:
    # Conservative escaping: avoid breaking markdown tables/lists.
    s = s.replace("\\", "\\\\")
    s = s.replace("|", "\\|")
    return s


def get_paragraph_num_info(p: Paragraph) -> Optional[Tuple[int, int]]:
    """
    Returns (numId, ilvl) if paragraph is part of a Word numbered/bulleted list.
    """
    ppr = p._p.pPr
    if ppr is None or ppr.numPr is None:
        return None
    num_id = None
    ilvl = 0
    if ppr.numPr.numId is not None and ppr.numPr.numId.val is not None:
        num_id = int(ppr.numPr.numId.val)
    if ppr.numPr.ilvl is not None and ppr.numPr.ilvl.val is not None:
        ilvl = int(ppr.numPr.ilvl.val)
    if num_id is None:
        return None
    return num_id, ilvl


def build_numbering_map(doc: Document) -> Dict[int, Dict[int, str]]:
    """
    numId -> ilvl -> numFmt (e.g. 'bullet', 'decimal', 'lowerRoman', ...)
    """
    m: Dict[int, Dict[int, str]] = {}
    numbering = doc.part.numbering_part.element
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

    def attr(el, name: str) -> Optional[str]:
        return el.get(f"{W}{name}")

    # Map abstractNumId -> {ilvl: numFmt}
    abs_map: Dict[int, Dict[int, str]] = {}
    for abs_num in numbering.iter():
        if abs_num.tag != f"{W}abstractNum":
            continue
        abs_id_s = attr(abs_num, "abstractNumId")
        if abs_id_s is None:
            continue
        abs_id = int(abs_id_s)
        lvl_map: Dict[int, str] = {}

        for lvl in abs_num.iterchildren():
            if lvl.tag != f"{W}lvl":
                continue
            ilvl_s = attr(lvl, "ilvl")
            if ilvl_s is None:
                continue
            ilvl = int(ilvl_s)

            fmt_val: Optional[str] = None
            for child in lvl.iterchildren():
                if child.tag == f"{W}numFmt":
                    fmt_val = attr(child, "val")
                    break
            if fmt_val:
                lvl_map[ilvl] = fmt_val

        abs_map[abs_id] = lvl_map

    # Map numId -> abstractNumId
    for num in numbering.iter():
        if num.tag != f"{W}num":
            continue
        num_id_s = attr(num, "numId")
        if num_id_s is None:
            continue
        num_id = int(num_id_s)

        abs_id: Optional[int] = None
        for child in num.iterchildren():
            if child.tag == f"{W}abstractNumId":
                v = attr(child, "val")
                if v is not None:
                    abs_id = int(v)
                break
        if abs_id is None:
            continue
        m[num_id] = dict(abs_map.get(abs_id, {}))

    return m


def iter_block_items(doc: Document) -> Iterator[Tuple[str, object]]:
    """
    Yield ("p", Paragraph) and ("tbl", Table) in document order.
    """
    parent = doc.element.body
    for child in parent.iterchildren():
        if isinstance(child, CT_P):
            yield "p", Paragraph(child, doc)
        elif isinstance(child, CT_Tbl):
            yield "tbl", Table(child, doc)


def style_name(p: Paragraph) -> str:
    return p.style.name if p.style is not None else ""


def is_heading(p: Paragraph, level: int) -> bool:
    sn = style_name(p)
    return sn == f"Heading {level}" or sn == f"Заголовок {level}"


def text_of(p: Paragraph) -> str:
    return norm_spaces((p.text or "").strip())


def normalize_formula_line(s: str) -> Optional[Tuple[str, str, List[str], Optional[str]]]:
    """
    Recognize a few key formulas from the пособие and return:
      (latex_block, caption, where_lines, purpose)
    to output in a nicer KaTeX-friendly way.

    Returns None if not a known formula line.
    """
    raw = norm_spaces(s)

    # 3) Approximate program length (Halstead)
    if re.search(r"^N\s*[≈~]\s*n1\s*log2\s*\(n1\)\s*\+\s*n2\s*log2\s*\(n2\)\s*,?\s*$", raw, re.IGNORECASE):
        latex = r"$$N \approx n_1 \cdot \log_2(n_1) + n_2 \cdot \log_2(n_2)$$"
        caption = "**Формула 3. Оценка длины программы (приближённая)**"
        where = [
            "- $n_1$ - число различных операторов",
            "- $n_2$ - число различных операндов",
        ]
        purpose = "**Назначение:** приближённая оценка длины программного модуля."
        return latex, caption, where, purpose

    # 1) Halstead volume
    if re.search(r"^V\s*=\s*N\s*[×x*]\s*log2\s*\(\s*n1\s*\+\s*n2\s*\)\s*\.?,?\s*$", raw, re.IGNORECASE):
        latex = r"$$V = N \cdot \log_2 (n_1 + n_2)$$"
        caption = "**Формула 1. Объём программы по Холстеду**"
        return latex, caption, [], None

    # 2) McCabe cyclomatic complexity
    if re.search(r"^V\\(G\\)\s*=\s*E\s*[–-]\s*N\s*\\+\s*2\s*,?\s*$", raw, re.IGNORECASE) or re.search(
        r"^V\(G\)\s*=\s*E\s*[–-]\s*N\s*\+\s*2\s*,?\s*$", raw, re.IGNORECASE
    ):
        latex = r"$$V(G) = E - N + 2$$"
        caption = "**Формула 2. Цикломатическая сложность Мак-Кейба**"
        where = [
            "- $E$ - количество дуг (рёбер) в управляющем графе",
            "- $N$ - количество вершин",
        ]
        purpose = "**Назначение:** оценка логической сложности алгоритма и числа независимых путей выполнения."
        return latex, caption, where, purpose

    return None


def runs_to_md(p: Paragraph) -> str:
    """
    Convert paragraph runs to Markdown inline text, preserving bold/italic.
    """
    parts: List[str] = []

    def append_text(txt: str) -> None:
        if not txt:
            return
        parts.append(txt)

    for run in p.runs:
        t = run.text or ""
        if not t:
            continue
        t = t.replace("\r", "").replace("\n", " ")
        # Keep leading/trailing spaces outside emphasis markers to avoid output like "*V *"
        m = re.match(r"^(\s*)(.*?)(\s*)$", t, flags=re.DOTALL)
        lead, core, tail = (m.group(1), m.group(2), m.group(3)) if m else ("", t, "")
        lead = norm_spaces(lead)
        core = escape_md_text(norm_spaces(core))
        tail = norm_spaces(tail)

        bold = bool(run.bold)
        italic = bool(run.italic)
        # Highlight is a common "important" emphasis in методичках; approximate as bold.
        if getattr(run.font, "highlight_color", None) is not None:
            bold = True

        # Don't wrap pure punctuation in emphasis - it produces noisy output like "*.*"
        has_word = bool(re.search(r"[0-9A-Za-zА-Яа-яЁё]", core))
        styled = core
        if has_word:
            if bold and italic:
                styled = f"***{core}***"
            elif bold:
                styled = f"**{core}**"
            elif italic:
                styled = f"*{core}*"

        append_text(f"{lead}{styled}{tail}")

    return "".join(parts).strip()


def table_to_md(tbl: Table) -> List[str]:
    rows = tbl.rows
    if not rows:
        return []

    def cell_text(cell) -> str:
        texts = []
        for p in cell.paragraphs:
            txt = runs_to_md(p)
            if txt:
                texts.append(txt)
        return escape_md_text(norm_spaces(" ".join(texts)))

    matrix: List[List[str]] = []
    for r in rows:
        matrix.append([cell_text(c) for c in r.cells])

    # normalize width
    width = max(len(r) for r in matrix) if matrix else 0
    for r in matrix:
        while len(r) < width:
            r.append("")

    if width == 0:
        return []

    header = matrix[0]
    body = matrix[1:] if len(matrix) > 1 else []

    out: List[str] = []
    out.append("| " + " | ".join(header) + " |")
    out.append("| " + " | ".join(["---"] * width) + " |")
    for r in body:
        out.append("| " + " | ".join(r) + " |")
    return out


@dataclass
class Section:
    id: str
    title: str
    markdown_file: str
    lines: List[str] = field(default_factory=list)


@dataclass
class Chapter:
    id: str
    title: str
    sections: List[Section] = field(default_factory=list)


def write_ts(chapters: List[Chapter]) -> None:
    def q(s: str) -> str:
        return s.replace("\\", "\\\\").replace("'", "\\'")

    lines: List[str] = []
    lines.append("import { Chapter } from '../types';")
    lines.append("")
    lines.append("export const chapters: Chapter[] = [")
    for ch in chapters:
        lines.append("  {")
        lines.append(f"    id: '{q(ch.id)}',")
        lines.append(f"    title: '{q(ch.title)}',")
        lines.append("    sections: [")
        for sec in ch.sections:
            lines.append("      {")
            lines.append(f"        id: '{q(sec.id)}',")
            lines.append(f"        title: '{q(sec.title)}',")
            lines.append(f"        markdownFile: '{q(sec.markdown_file)}',")
            lines.append("      },")
        lines.append("    ],")
        lines.append("  },")
    lines.append("];")
    lines.append("")
    CHAPTERS_TS.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not DOCX_PATH.exists():
        raise SystemExit(f"DOCX not found: {DOCX_PATH}")

    doc = Document(str(DOCX_PATH))
    numbering_map = build_numbering_map(doc)

    chapters: List[Chapter] = []
    current_ch: Optional[Chapter] = None
    current_sec: Optional[Section] = None
    in_toc = False
    started_main = False
    skip_where_once = False

    # Helpers
    def start_chapter(title: str, explicit_id: Optional[str] = None) -> Chapter:
        nonlocal current_ch, current_sec
        if current_sec is not None:
            finalize_section()
        current_sec = None

        ch_id = explicit_id or slugify_ru(title)
        current_ch = Chapter(id=ch_id, title=title)
        chapters.append(current_ch)
        return current_ch

    def start_section(title: str, chapter_num: Optional[int] = None, special_prefix: Optional[str] = None) -> Section:
        nonlocal current_sec, current_ch
        if current_ch is None:
            # Fallback: create a chapter bucket
            start_chapter("Материалы", explicit_id="materials")

        if current_sec is not None:
            finalize_section()

        if special_prefix:
            sec_id = f"{special_prefix}-1"
            file_name = f"{special_prefix}-1.md"
        else:
            slug = slugify_ru(title)
            if chapter_num is None:
                sec_id = slug
                file_name = f"{slug}.md"
            else:
                sec_id = f"chapter-{chapter_num}-{slug}"
                file_name = f"chapter-{chapter_num}-{slug}.md"

        md_file = f"chapters/{file_name}"
        current_sec = Section(id=sec_id, title=title, markdown_file=md_file, lines=[f"# {title}", ""])
        current_ch.sections.append(current_sec)
        return current_sec

    def finalize_section() -> None:
        nonlocal current_sec
        if current_sec is None:
            return
        # trim trailing blanks
        while current_sec.lines and current_sec.lines[-1] == "":
            current_sec.lines.pop()
        current_sec.lines.append("")  # newline at EOF
        current_sec = None

    # Track chapter number for numbered chapters (1..N)
    chapter_num: Optional[int] = None
    last_numbered: int = 0

    for kind, obj in iter_block_items(doc):
        if kind == "p":
            p: Paragraph = obj  # type: ignore[assignment]
            txt = text_of(p)
            if not txt:
                # preserve paragraph spacing inside a section
                if current_sec is not None and current_sec.lines and current_sec.lines[-1] != "":
                    current_sec.lines.append("")
                continue

            # Heading 1 is usually book title — ignore.
            if is_heading(p, 1):
                continue

            # Heading 2: top-level parts
            if is_heading(p, 2):
                started_main = True
                if TOC_TITLE_RE.match(txt):
                    in_toc = True
                    continue
                in_toc = False

                if txt.upper() == "ВВЕДЕНИЕ":
                    chapter_num = None
                    start_chapter("Введение", explicit_id="introduction")
                    start_section("Введение", special_prefix="introduction")
                    continue
                if txt.upper() == "ЗАКЛЮЧЕНИЕ":
                    chapter_num = None
                    start_chapter("Заключение", explicit_id="conclusion")
                    start_section("Заключение", special_prefix="conclusion")
                    continue
                if txt.upper() == "СПИСОК ЛИТЕРАТУРЫ":
                    chapter_num = None
                    start_chapter("Список литературы", explicit_id="references")
                    start_section("Список литературы", special_prefix="references")
                    continue

                m = HEADING_RE.match(txt)
                if m:
                    last_numbered = int(m.group(1))
                    chapter_num = last_numbered
                    ch_title = txt
                else:
                    # Some docs omit the number for Chapter 2 title — keep sequential numbering.
                    last_numbered += 1
                    chapter_num = last_numbered
                    ch_title = f"{chapter_num}. {txt}"

                start_chapter(ch_title, explicit_id=f"chapter-{chapter_num}")
                continue

            # Heading 3: section start (one md per Heading 3)
            if is_heading(p, 3):
                if in_toc:
                    continue
                if chapter_num is None:
                    # introduction/conclusion/references bucket
                    start_section(txt, special_prefix=(current_ch.id if current_ch else None))
                else:
                    start_section(txt, chapter_num=chapter_num)
                continue

            # Ignore TOC content (lines with dot leaders + trailing page numbers, etc.)
            if in_toc:
                continue

            # Ignore any front-matter before the first real Heading 2 (title pages, etc.)
            if not started_main:
                continue

            if current_sec is None:
                # If we haven't started a section yet, create a generic one under current chapter.
                if current_ch is None:
                    start_chapter("Материалы", explicit_id="materials")
                start_section(current_ch.title, chapter_num=chapter_num)

            # Heading 4+ inside a section
            if is_heading(p, 4):
                current_sec.lines.append(f"## {txt}")
                current_sec.lines.append("")
                continue
            if is_heading(p, 5):
                current_sec.lines.append(f"### {txt}")
                current_sec.lines.append("")
                continue
            if is_heading(p, 6):
                current_sec.lines.append(f"#### {txt}")
                current_sec.lines.append("")
                continue

            # Regular paragraph: try formula normalization first
            formula = normalize_formula_line(txt)
            if formula:
                latex, caption, where, purpose = formula
                current_sec.lines.append(latex)
                current_sec.lines.append("")
                current_sec.lines.append(caption)
                current_sec.lines.append("")
                if where:
                    current_sec.lines.append("где:")
                    current_sec.lines.extend(where)
                    current_sec.lines.append("")
                if purpose:
                    current_sec.lines.append(purpose)
                    current_sec.lines.append("")
                skip_where_once = True
                continue

            if skip_where_once:
                # If we already inserted a normalized formula with "где:", skip the following
                # Word sentence starting with "где ..." to avoid duplication.
                if re.match(r"^\s*где\b", txt, flags=re.IGNORECASE):
                    skip_where_once = False
                    continue
                skip_where_once = False

            # List handling (Word numbering)
            num_info = get_paragraph_num_info(p)
            if num_info:
                num_id, ilvl = num_info
                fmt = numbering_map.get(num_id, {}).get(ilvl, "decimal")
                indent = "  " * ilvl
                bullet = fmt == "bullet"
                prefix = "- " if bullet else "1. "
                content = runs_to_md(p)
                if not content:
                    content = escape_md_text(txt)
                current_sec.lines.append(f"{indent}{prefix}{content}")
                continue

            # Normal paragraph
            content = runs_to_md(p)
            if not content:
                content = escape_md_text(txt)
            current_sec.lines.append(content)
            current_sec.lines.append("")

        elif kind == "tbl":
            if in_toc:
                continue
            # Ignore any front-matter before the first real Heading 2 (title pages, etc.)
            if not started_main:
                continue
            if current_sec is None:
                # same fallback as for paragraphs
                if current_ch is None:
                    start_chapter("Материалы", explicit_id="materials")
                start_section(current_ch.title, chapter_num=chapter_num)
            tbl: Table = obj  # type: ignore[assignment]
            md_lines = table_to_md(tbl)
            if md_lines:
                current_sec.lines.extend(md_lines)
                current_sec.lines.append("")

    finalize_section()

    # Write markdown files
    OUT_PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    OUT_SRC_DIR.mkdir(parents=True, exist_ok=True)

    generated_files: List[str] = []
    for ch in chapters:
        for sec in ch.sections:
            rel = sec.markdown_file.replace("chapters/", "")
            generated_files.append(rel)

            content = "\n".join(sec.lines).rstrip() + "\n"

            (OUT_PUBLIC_DIR / rel).write_text(content, encoding="utf-8")
            (OUT_SRC_DIR / rel).write_text(content, encoding="utf-8")

    # Remove stale markdowns not referenced
    gen_set = set(generated_files)
    for d in (OUT_PUBLIC_DIR, OUT_SRC_DIR):
        for md in d.glob("*.md"):
            if md.name not in gen_set:
                md.unlink()

    # Update chapters.ts
    write_ts(chapters)

    print(f"Chapters: {len(chapters)}")
    print(f"Sections: {sum(len(ch.sections) for ch in chapters)}")
    print(f"Markdown files written: {len(generated_files)} (mirrored to src/ and public/)")


if __name__ == "__main__":
    main()



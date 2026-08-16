#!/usr/bin/env python3
"""
Convert a Chinese resume Markdown file to a one-page A4 PDF.

Default Chinese visual style matches「定稿中文一页简历样式」:
gray bar section headings with left accent, name underline,
italic project intros with left rule.
"""

from __future__ import annotations

import argparse
import base64
import html
import mimetypes
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


FIXED_LINE_HEIGHT = "1.3"

PRESETS = {
    "standard": {
        "margin_top": "1.0cm",
        "margin_x": "2.0cm",
        "margin_bottom": "0.55cm",
        "line_height": "1.26",
        "section_margin_after": "2pt",
        "paragraph_margin_after": "2pt",
        "body_padding_top": "10mm",
        "body_font_size": "9.1pt",
        "photo_width": "52pt",
        "photo_height": "76pt",
        "h2_margin_top": "5pt",
        "h2_font_size": "11pt",
        "task_margin_after": "3.5pt",
        "project_group_margin_top": "4pt",
        "project_group_margin_after": "1.5pt",
        "project_intro_font_size": "8.6pt",
        "project_intro_margin_after": "2pt",
        "company_gap_after_task": "5pt",
        "name_font_size": "17pt",
        "contact_font_size": "10pt",
        "row_heading_font_size": "10.8pt",
        "skill_item_margin_after": "2pt",
    },
    "fill": {
        "margin_top": "1.0cm",
        "margin_x": "2.0cm",
        "margin_bottom": "0.5cm",
        "line_height": "1.28",
        "section_margin_after": "3pt",
        "paragraph_margin_after": "2.5pt",
        "body_padding_top": "11mm",
        "body_font_size": "9.3pt",
        "photo_width": "52pt",
        "photo_height": "76pt",
        "h2_margin_top": "5pt",
        "h2_font_size": "11pt",
        "task_margin_after": "4pt",
        "project_group_margin_top": "4pt",
        "project_group_margin_after": "1.5pt",
        "project_intro_font_size": "8.6pt",
        "project_intro_margin_after": "2pt",
        "company_gap_after_task": "5pt",
        "name_font_size": "17pt",
        "contact_font_size": "10pt",
        "row_heading_font_size": "10.8pt",
        "skill_item_margin_after": "2pt",
    },
    "tight": {
        "margin_top": "1.0cm",
        "margin_x": "2.0cm",
        "margin_bottom": "0.45cm",
        "line_height": "1.24",
        "section_margin_after": "1.5pt",
        "paragraph_margin_after": "1.5pt",
        "body_padding_top": "9mm",
        "body_font_size": "8.85pt",
        "photo_width": "50pt",
        "photo_height": "73pt",
        "h2_margin_top": "5pt",
        "h2_font_size": "11pt",
        "task_margin_after": "2pt",
        "project_group_margin_top": "4pt",
        "project_group_margin_after": "1.5pt",
        "project_intro_font_size": "8.6pt",
        "project_intro_margin_after": "2pt",
        "company_gap_after_task": "5pt",
        "name_font_size": "17pt",
        "contact_font_size": "10pt",
        "row_heading_font_size": "10.8pt",
        "skill_item_margin_after": "2pt",
    },
    "compact": {
        "margin_top": "1.0cm",
        "margin_x": "2.0cm",
        "margin_bottom": "0.4cm",
        "line_height": "1.22",
        "section_margin_after": "1pt",
        "paragraph_margin_after": "1pt",
        "body_padding_top": "9mm",
        "body_font_size": "8.6pt",
        "photo_width": "50pt",
        "photo_height": "73pt",
        "h2_margin_top": "4pt",
        "h2_font_size": "11pt",
        "task_margin_after": "1pt",
        "project_group_margin_top": "3pt",
        "project_group_margin_after": "1pt",
        "project_intro_font_size": "8.3pt",
        "project_intro_margin_after": "1.5pt",
        "company_gap_after_task": "4pt",
        "name_font_size": "17pt",
        "contact_font_size": "10pt",
        "row_heading_font_size": "10.8pt",
        "skill_item_margin_after": "1.5pt",
    },
    # 内容偏多的一页简历：比 compact 更紧；靠略窄边距减少换行，再调字号填满 1 页。
    "onepage_dense": {
        "margin_top": "0.88cm",
        "margin_x": "1.7cm",
        "margin_bottom": "0.42cm",
        "line_height": "1.20",
        "section_margin_after": "1pt",
        "paragraph_margin_after": "1pt",
        "body_padding_top": "8.2mm",
        "body_font_size": "8.55pt",
        "photo_width": "48pt",
        "photo_height": "70pt",
        "h2_margin_top": "3.5pt",
        "h2_font_size": "10.5pt",
        "task_margin_after": "1pt",
        "project_group_margin_top": "3pt",
        "project_group_margin_after": "1.2pt",
        "project_intro_font_size": "8.2pt",
        "project_intro_margin_after": "1.2pt",
        "company_gap_after_task": "3.5pt",
        "name_font_size": "16.2pt",
        "contact_font_size": "9.4pt",
        "row_heading_font_size": "10.5pt",
        "skill_item_margin_after": "1.5pt",
    },
}
BOTTOM_GAP_MIN_MM = 3.0
BOTTOM_GAP_MAX_MM = 20.0


STYLE_SUFFIX_PATTERN = re.compile(
    r"(?:[_-](?:脚本|美化|填充|大字号|reportlab|draft|v\d+)(?:版)?)$|(?:reportlab)$",
    re.I,
)
TABLE_HEADER_KEYWORDS = {
    "公司",
    "岗位",
    "岗位名称",
    "时间",
    "学校",
    "学历",
    "专业",
}
REQUIRED_SKILL_LABELS = ["工作技能", "数据技能", "AI技能", "语言能力"]
ENGLISH_SKILL_LABELS = ["Professional Skills", "Data Skills", "Digital Skills", "Languages"]
ENGLISH_AI_SKILL_LABELS = ["Professional Skills", "Data Skills", "AI Skills", "Languages"]
SKILL_LABEL_SETS = [REQUIRED_SKILL_LABELS, ENGLISH_SKILL_LABELS, ENGLISH_AI_SKILL_LABELS]
FORBIDDEN_RESUME_SUMMARY_LABELS = ["求职优势", "求职摘要", "个人总结"]
PROJECT_GROUP_RE = re.compile(r"^项目[一二三四五六七八九十百千\d]+[：:]\s*(.+)$")
SUB_ITEM_RE = re.compile(r"^([①②③④⑤⑥⑦⑧⑨⑩]|[一二三四五六七八九十]+|\d+)[）)]\s*(.+)$")
BULLET_TASK_RE = re.compile(r"^[·•]\s+(.+)$")
PROJECT_TASK_RE = re.compile(r"^\*\*(.+?)\*\*[：:]\s*(.+)$")
DATE_END_PATTERN = r"(?:\d{4}\.\d{2}|至今|Present)"
SECTION_CANONICAL = {
    "教育经历": "教育经历",
    "Education": "教育经历",
    "实习经历": "实习经历",
    "Experience": "实习经历",
    "Internship Experience": "实习经历",
    "Professional Experience": "实习经历",
    "相关技能": "相关技能",
    "Skills": "相关技能",
    "Relevant Skills": "相关技能",
}
SECTION_DISPLAY = {
    "教育经历": ("教育经历", "Education"),
    "实习经历": ("实习经历", "Experience"),
    "相关技能": ("相关技能", "Skills", "Relevant Skills"),
}


def canonicalize_section_name(name: str) -> str | None:
    return SECTION_CANONICAL.get(name.strip())


def section_heading_aliases(canonical: str) -> tuple[str, ...]:
    return SECTION_DISPLAY.get(canonical, (canonical,))


def parse_bold_project_header(line: str) -> str | None:
    match = re.fullmatch(r"\*\*((?:项目|Project)[^*]+)\*\*", line.strip())
    if match:
        return match.group(1).strip()
    return None


def is_bold_project_header(line: str) -> bool:
    return parse_bold_project_header(line) is not None


def parse_project_group(line: str) -> tuple[str, str, str] | None:
    match = re.match(
        r"^((?:项目[一二三四五六七八九十百千\d]+|Project\s*\d+))[：:]\s*(.+)$",
        line.strip(),
    )
    if not match:
        return None
    label = match.group(1)
    rest = match.group(2).strip()
    title, separator, intro = rest.partition("：")
    if not separator:
        title, separator, intro = rest.partition(":")
    if separator:
        return label, title.strip(), intro.strip()
    return label, rest, ""


def match_sub_item(line: str) -> re.Match[str] | None:
    return SUB_ITEM_RE.match(line.strip())


def match_project_task(line: str) -> re.Match[str] | None:
    return PROJECT_TASK_RE.match(line.strip())


def is_project_task_line(line: str) -> bool:
    return bool(BULLET_TASK_RE.match(line.strip()) or match_project_task(line))


def sub_item_number(value: str) -> int | None:
    if value.isdigit():
        return int(value)
    mapping = {
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
        "十": 10,
    }
    if len(value) == 1 and value in mapping:
        return mapping[value]
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert resume Markdown to PDF with an A4 one-page layout."
    )
    parser.add_argument("input", type=Path, help="Input Markdown resume path.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output PDF path. Defaults to 公司+姓名+岗位.pdf when it can be inferred.",
    )
    parser.add_argument(
        "--preset",
        choices=PRESETS.keys(),
        default="standard",
        help=(
            "Layout preset: standard; fill for sparse resumes; tight for near-overflow; "
            "compact for dense multi-project; onepage_dense for content-heavy one-pagers."
        ),
    )
    parser.add_argument(
        "--browser",
        type=Path,
        help="Optional path to msedge/chrome/chromium executable.",
    )
    parser.add_argument(
        "--keep-html",
        action="store_true",
        help="Also write the intermediate HTML next to the PDF for inspection.",
    )
    parser.add_argument(
        "--allow-multipage",
        action="store_true",
        help="Export preview PDFs even when the result is not exactly one page.",
    )
    return parser.parse_args()


def clean_filename_part(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\n\r\t]+', "", value).strip()
    return re.sub(r"\s+", " ", cleaned)


def extract_name(markdown_text: str, fallback: str | None = None) -> str | None:
    for line in markdown_text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return clean_filename_part(match.group(1).strip("` "))
    return clean_filename_part(fallback) if fallback else None


def extract_role(markdown_text: str) -> str | None:
    for line in markdown_text.splitlines():
        match = re.search(
            r"(?:应聘|Applying for|Target Role|Target)[：:]\s*(.+)$",
            line,
            flags=re.I,
        )
        if match:
            role = re.split(r"[/,，|｜]", match.group(1), maxsplit=1)[0]
            return clean_filename_part(role)
    return None


def infer_company_name_role(input_path: Path, markdown_text: str) -> tuple[str | None, str | None, str | None]:
    stem = re.sub(r"_[^_]+版$", "", input_path.stem)
    parts = [clean_filename_part(part) for part in stem.split("+") if clean_filename_part(part)]

    company = None
    name = None
    role = None

    if len(parts) >= 4:
        name = parts[1]
        role = parts[2]
        company = parts[-1]
    elif len(parts) == 3:
        company, name, role = parts

    name = extract_name(markdown_text, name)
    role = role or extract_role(markdown_text)
    return company, name, role


def default_output_path(input_path: Path, markdown_text: str) -> Path:
    company, name, role = infer_company_name_role(input_path, markdown_text)
    if company and name and role:
        return input_path.parent / f"{company}+{name}+{role}.pdf"
    return input_path.with_suffix(".pdf")


def has_style_suffix(path: Path) -> bool:
    return bool(STYLE_SUFFIX_PATTERN.search(path.stem))


def validate_output_filename(output_path: Path) -> list[str]:
    errors = []
    parts = [part for part in output_path.stem.split("+") if part.strip()]
    if len(parts) != 3:
        errors.append(
            "Output PDF filename must follow 公司+姓名+岗位.pdf. "
            f"Current filename: {output_path.name}"
        )
    if has_style_suffix(output_path):
        errors.append(
            "Output PDF filename must not include style/version suffixes such as "
            "_脚本版, _美化版, _填充版, _大字号版, or reportlab."
        )
    return errors


def iter_section_lines(markdown_text: str, section_name: str) -> list[str]:
    lines = markdown_text.splitlines()
    section_lines: list[str] = []
    in_section = False
    aliases = section_heading_aliases(canonicalize_section_name(section_name) or section_name)
    for line in lines:
        heading = re.match(r"^##\s+(.+?)\s*$", line.strip())
        if heading:
            heading_name = heading.group(1).strip()
            if heading_name in aliases or canonicalize_section_name(heading_name) == (
                canonicalize_section_name(section_name) or section_name
            ):
                in_section = True
                continue
            if in_section:
                break
        if in_section:
            section_lines.append(line)
    return section_lines


def validate_image_paths(markdown_text: str, base_dir: Path) -> list[str]:
    errors = []
    image_matches = list(re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", markdown_text))
    personal_photo_matches = [
        match for match in image_matches if match.group(1).strip() == "个人照片"
    ]

    if len(image_matches) != 1:
        errors.append(
            "Resume Markdown must include exactly one personal headshot image: "
            "![个人照片](relative/path/to/photo.png)."
        )
    elif len(personal_photo_matches) != 1:
        errors.append("The required headshot image alt text must be exactly '个人照片'.")

    for match in personal_photo_matches:
        image_path = match.group(2).strip()
        if re.match(r"^(?:https?://|data:|file:)", image_path):
            errors.append(
                "Personal photo must use a workspace-local relative image path, "
                f"not an external/data/file URL: {image_path}"
            )
            continue
        path = Path(image_path)
        if path.is_absolute():
            errors.append(
                f"Personal photo path must be relative to the workspace/resume file: {image_path}"
            )
            continue
        if not (base_dir / path).exists():
            errors.append(f"Personal photo path does not exist: {image_path}")
    return errors


def validate_no_markdown_tables(markdown_text: str) -> list[str]:
    lines = markdown_text.splitlines()
    errors = []
    for index, line in enumerate(lines[:-1], start=1):
        if "|" in line and is_table_separator(lines[index]):
            header_cells = {
                cell.strip().strip("*`")
                for cell in line.strip().strip("|").split("|")
                if cell.strip()
            }
            if header_cells & TABLE_HEADER_KEYWORDS:
                errors.append(
                    "Avoid visible table headers for aligned resume fields; "
                    f"convert the table near line {index} to aligned text rows."
                )
            else:
                errors.append(
                    f"Markdown table found near line {index}; resume layout should use headings, "
                    "aligned text rows, and bullets instead of tables."
                )
    return errors


def validate_section_separators(markdown_text: str) -> list[str]:
    errors = []
    lines = markdown_text.splitlines()
    required_before = []
    for canonical in ("实习经历", "相关技能"):
        required_before.extend(f"## {alias}" for alias in section_heading_aliases(canonical))
    for heading in required_before:
        try:
            index = next(
                index for index, line in enumerate(lines) if line.strip() == heading
            )
        except StopIteration:
            continue
        if index == 0 or lines[index - 1].strip() != "---":
            errors.append(
                f"Add one separator line '---' immediately before {heading[3:]}."
            )

    for index, line in enumerate(lines, start=1):
        if re.fullmatch(r"\s*(?:\*{3,}|_{3,})\s*", line):
            errors.append(
                "Use only '---' as the section separator line "
                f"(found another horizontal rule near line {index})."
            )
    return errors


def _match_skill_label_set(skill_lines: list[str], label_sets: list[list[str]]) -> list[str]:
    last_errors: list[str] | None = None
    for label_set in label_sets:
        if len(skill_lines) != len(label_set):
            continue
        errors = []
        for index, (line, label) in enumerate(zip(skill_lines, label_set), start=1):
            pattern = rf"^{index}\.\s*\*\*{re.escape(label)}\*\*[：:].+"
            if not re.match(pattern, line):
                errors.append(
                    f"Skill line {index} must be a single line like '{index}. **{label}**: ...'."
                )
        if not errors:
            return []
        last_errors = errors
    if last_errors is not None:
        return last_errors
    return [
        "Skill lines must use either Chinese labels "
        "(工作技能/数据技能/AI技能/语言能力) or English labels "
        "(Professional Skills/Data Skills/Digital Skills|AI Skills/Languages)."
    ]


def validate_skills_section(markdown_text: str) -> list[str]:
    section_lines = iter_section_lines(markdown_text, "相关技能")
    if not section_lines:
        return ["The resume must include a Skills / 相关技能 section."]

    if any(re.match(r"^\s*###\s+", line) for line in section_lines):
        return [
            "The Skills / 相关技能 section must use one-line ordered items, not ### subheadings."
        ]

    skill_lines = [
        line.strip()
        for line in section_lines
        if line.strip() and not re.fullmatch(r"\s*---\s*", line)
    ]
    expected_count = len(REQUIRED_SKILL_LABELS)
    if len(skill_lines) != expected_count:
        return [
            "The Skills / 相关技能 section must contain exactly 4 one-line items "
            "(Chinese labels or: Professional Skills / Data Skills / "
            "Digital Skills|AI Skills / Languages)."
        ]

    return _match_skill_label_set(skill_lines, SKILL_LABEL_SETS)


def validate_no_resume_summary(markdown_text: str) -> list[str]:
    errors = []
    for index, line in enumerate(markdown_text.splitlines(), start=1):
        stripped = line.strip().lstrip("#>*-0123456789. ")
        stripped = stripped.strip("*` ")
        for label in FORBIDDEN_RESUME_SUMMARY_LABELS:
            if stripped.startswith(f"{label}：") or stripped.startswith(f"{label}:"):
                errors.append(
                    f"Do not include '{label}' sections or inline summaries in the resume "
                    f"(found near line {index})."
                )
    return errors


def validate_internship_numbered_items(markdown_text: str) -> list[str]:
    section_lines = iter_section_lines(markdown_text, "实习经历")
    errors = []
    current_header: str | None = None
    item_count = 0
    expected_number = 1
    sub_expected_number = 1

    def flush() -> None:
        nonlocal item_count, current_header, expected_number, sub_expected_number
        # No hard cap on numbered items per company; one-page fit is enforced by
        # PDF page/layout checks. Prefer tight/compact presets over merging items.
        item_count = 0
        expected_number = 1
        sub_expected_number = 1

    for line_number, raw in enumerate(section_lines, start=1):
        line = raw.strip()
        if parse_project_group(line) or is_bold_project_header(line):
            sub_expected_number = 1
            continue

        bullet_task = BULLET_TASK_RE.match(line)
        if bullet_task or match_project_task(line):
            item_count += 1
            continue

        sub_item = match_sub_item(line)
        if sub_item:
            actual_number = sub_item_number(sub_item.group(1))
            if actual_number is not None and actual_number != sub_expected_number:
                location = f" under '{current_header}'" if current_header else ""
                errors.append(
                    "Project sub-items must restart at 1） within each project group and increase "
                    f"sequentially; expected {sub_expected_number}） near 实习经历 line {line_number}, "
                    f"found {actual_number}）{location}."
                )
            if actual_number is not None:
                sub_expected_number = actual_number + 1
            else:
                sub_expected_number += 1
            item_count += 1
            continue

        is_header = (
            bool(line)
            and not re.match(r"^(?:[-*]|\d+\.)\s+", line)
            and not is_bold_project_header(line)
            and not parse_project_group(line)
            and (line.startswith("**") or re.search(rf"\d{{4}}\.\d{{2}}|{DATE_END_PATTERN}", line))
        )
        if is_header:
            flush()
            current_header = re.sub(r"[*`]", "", line)
            continue

        if re.match(r"^[-*]\s+", line):
            location = f" under '{current_header}'" if current_header else ""
            errors.append(
                "Internship experience items must use ordered Markdown list syntax "
                f"('1.', '2.', ...) or project sub-items ('1）', '2）', ...), not '-' or '*' "
                f"bullets near 实习经历 line {line_number}{location}."
            )
            continue

        ordered = re.match(r"^(\d+)\.\s+", line)
        if ordered:
            actual_number = int(ordered.group(1))
            if actual_number != expected_number:
                location = f" under '{current_header}'" if current_header else ""
                errors.append(
                    "Internship ordered items must restart at 1 under each company and increase "
                    f"sequentially; expected {expected_number}. near 实习经历 line {line_number}, "
                    f"found {actual_number}{location}."
                )
            expected_number = actual_number + 1
            sub_expected_number = 1
            item_count += 1
    flush()
    return errors


def validate_ordered_list_numbering(markdown_text: str) -> list[str]:
    errors = []
    expected: int | None = None

    for line_number, raw in enumerate(markdown_text.splitlines(), start=1):
        line = raw.strip()
        ordered = re.match(r"^(\d+)\.\s+", line)
        unordered = re.match(r"^[-*]\s+", line)

        if ordered:
            actual = int(ordered.group(1))
            if expected is None:
                expected = 1
            if actual != expected:
                errors.append(
                    f"Ordered list numbering must increase sequentially; "
                    f"expected {expected}. near line {line_number}, found {actual}."
                )
            expected = actual + 1
            continue

        if match_sub_item(line) or parse_project_group(line) or is_bold_project_header(line) or is_project_task_line(line):
            continue

        if not line or raw.startswith((" ", "\t")):
            continue

        if unordered:
            expected = None
            continue

        expected = None

    return errors


def validate_resume_markdown(
    markdown_text: str,
    base_dir: Path,
    output_path: Path,
) -> list[str]:
    errors = []
    errors.extend(validate_output_filename(output_path))
    errors.extend(validate_image_paths(markdown_text, base_dir))
    errors.extend(validate_no_resume_summary(markdown_text))
    errors.extend(validate_section_separators(markdown_text))
    errors.extend(validate_no_markdown_tables(markdown_text))
    errors.extend(validate_skills_section(markdown_text))
    errors.extend(validate_internship_numbered_items(markdown_text))
    errors.extend(validate_ordered_list_numbering(markdown_text))
    return errors


def measure_bottom_gap_mm(pdf_path: Path) -> float | None:
    try:
        import fitz  # type: ignore

        document = fitz.open(str(pdf_path))
        if len(document) == 0:
            return None
        page = document[-1]
        bottoms = [
            block[3]
            for block in page.get_text("blocks")
            if len(block) >= 5 and str(block[4]).strip()
        ]
        if not bottoms:
            return None
        return (page.rect.height - max(bottoms)) * 25.4 / 72
    except Exception:
        return None


def rectangles_overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    left = max(a[0], b[0])
    top = max(a[1], b[1])
    right = min(a[2], b[2])
    bottom = min(a[3], b[3])
    return right - left > 0.5 and bottom - top > 0.5


def validate_pdf_photo_layout(pdf_path: Path) -> list[str]:
    try:
        import fitz  # type: ignore

        document = fitz.open(str(pdf_path))
        image_blocks: list[tuple[int, tuple[float, float, float, float]]] = []
        text_blocks: list[tuple[int, tuple[float, float, float, float]]] = []

        for page_index, page in enumerate(document, start=1):
            for block in page.get_text("dict").get("blocks", []):
                bbox = tuple(float(value) for value in block.get("bbox", ()))
                if len(bbox) != 4:
                    continue
                if block.get("type") == 1:
                    image_blocks.append((page_index, bbox))
                elif block.get("type") == 0:
                    text = "".join(
                        span.get("text", "")
                        for line in block.get("lines", [])
                        for span in line.get("spans", [])
                    )
                    if text.strip():
                        text_blocks.append((page_index, bbox))

        if len(image_blocks) != 1:
            return [
                "Exported PDF must contain exactly one personal headshot image; "
                f"detected {len(image_blocks)} image blocks."
            ]

        image_page, image_bbox = image_blocks[0]
        for text_page, text_bbox in text_blocks:
            if image_page == text_page and rectangles_overlap(image_bbox, text_bbox):
                return [
                    "Personal photo overlaps resume text in the exported PDF; "
                    "move or resize the photo before delivery."
                ]
        return []
    except Exception as exc:
        return [f"Could not validate PDF personal photo layout: {exc}"]


def validate_pdf_layout(pdf_path: Path) -> tuple[list[str], float | None]:
    photo_errors = validate_pdf_photo_layout(pdf_path)
    bottom_gap_mm = measure_bottom_gap_mm(pdf_path)
    if bottom_gap_mm is None:
        return photo_errors + ["Could not measure PDF bottom whitespace for skill validation."], None
    if bottom_gap_mm < BOTTOM_GAP_MIN_MM or bottom_gap_mm > BOTTOM_GAP_MAX_MM:
        return photo_errors + [
            "The last text line must land roughly 3-20mm above the page bottom; "
            f"current bottom whitespace is {bottom_gap_mm:.1f}mm."
        ], bottom_gap_mm
    return photo_errors, bottom_gap_mm


def count_pdf_pages(pdf_path: Path) -> int:
    try:
        from pypdf import PdfReader

        return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        pass

    try:
        from PyPDF2 import PdfReader

        return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        pass

    data = pdf_path.read_bytes()
    # Count concrete page objects, excluding the /Pages tree object.
    return len(re.findall(rb"/Type\s*/Page(?!s)\b", data))


def inline_markdown(text: str) -> str:
    escaped = html.escape(text.strip())
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def parse_row_heading(line: str, middle_trim_chars: str = "") -> tuple[str, str, str] | None:
    match = re.match(
        rf"^\*\*(?P<company>[^*]+)\*\*\s*(?P<middle>.+?)\s*(?P<date>\d{{4}}\.\d{{2}}\s*-\s*{DATE_END_PATTERN})\s*$",
        line.replace("\u3000", " "),
    )
    if not match:
        return None

    company = match.group("company").strip()
    role = re.sub(r"\s+", " ", match.group("middle")).strip().strip(middle_trim_chars)
    date = re.sub(r"\s+", "", match.group("date")).strip()
    if not company or not role or not date:
        return None
    return company, role, date


def render_row_heading(line: str, middle_trim_chars: str = "") -> str | None:
    parsed = parse_row_heading(line, middle_trim_chars)
    if not parsed:
        return None
    company, role, date = parsed
    return (
        '<p class="row-heading row-heading-grid">'
        f'<span class="row-company">{inline_markdown(company)}</span>'
        f'<span class="row-role">{inline_markdown(role)}</span>'
        f'<span class="row-date">{inline_markdown(date)}</span>'
        "</p>"
    )


def resolve_image_src(image_path: str, base_dir: Path) -> str:
    if re.match(r"^(?:https?://|data:|file:)", image_path):
        return html.escape(image_path, quote=True)
    path = Path(image_path)
    if not path.is_absolute():
        path = base_dir / path
    if not path.exists():
        return html.escape(image_path, quote=True)
    mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and set(stripped.replace("|", "").replace(" ", "")) <= {"-", ":"}


def render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)

    header = rows[0]
    body = rows[2:] if len(rows) > 1 and is_table_separator(lines[1]) else rows[1:]
    head_html = "".join(f"<th>{inline_markdown(cell)}</th>" for cell in header)
    body_html = []
    for row in body:
        body_html.append(
            "<tr>" + "".join(f"<td>{inline_markdown(cell)}</td>" for cell in row) + "</tr>"
        )
    return f"<table><thead><tr>{head_html}</tr></thead><tbody>{''.join(body_html)}</tbody></table>"


def markdown_to_body(markdown_text: str, base_dir: Path) -> str:
    lines = markdown_text.splitlines()
    output: list[str] = []
    in_ul = False
    in_ol = False
    seen_h1 = False
    contact_lines_remaining = 0
    current_section: str | None = None
    i = 0

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            output.append("</ul>")
            in_ul = False
        if in_ol:
            output.append("</ol>")
            in_ol = False

    def collect_list_item_text(first_line: str, start_index: int) -> tuple[str, int]:
        parts = [inline_markdown(first_line)]
        next_index = start_index
        while next_index < len(lines):
            continuation = lines[next_index]
            stripped = continuation.strip()
            if not stripped:
                break
            if not continuation.startswith((" ", "\t")):
                break
            if (
                re.match(r"^(?:[-*]|\d+\.)\s+", stripped)
                or match_sub_item(stripped)
                or parse_project_group(stripped)
                or is_bold_project_header(stripped)
                or is_project_task_line(stripped)
            ):
                break
            parts.append(inline_markdown(stripped))
            next_index += 1
        return "<br>".join(parts), next_index

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()

        if not line:
            close_lists()
            if contact_lines_remaining > 0:
                contact_lines_remaining = 0
            i += 1
            continue

        if "|" in line and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            close_lists()
            table_lines = [lines[i], lines[i + 1]]
            i += 2
            while i < len(lines) and "|" in lines[i].strip():
                table_lines.append(lines[i])
                i += 1
            output.append(render_table(table_lines))
            continue

        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", line):
            close_lists()
            output.append("<hr>")
            i += 1
            continue

        image = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", line)
        if image:
            close_lists()
            contact_lines_remaining = 0
            alt = html.escape(image.group(1), quote=True)
            src = resolve_image_src(image.group(2).strip(), base_dir)
            output.append(f'<p class="photo"><img src="{src}" alt="{alt}"></p>')
            i += 1
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            close_lists()
            level = len(heading.group(1))
            heading_text = heading.group(2).strip()
            text = inline_markdown(heading_text)
            output.append(f"<h{level}>{text}</h{level}>")
            if level != 1:
                contact_lines_remaining = 0
            if level == 2:
                heading_clean = re.sub(r"[*`]", "", heading_text).strip()
                current_section = canonicalize_section_name(heading_clean) or heading_clean
            if level == 1 and not seen_h1:
                seen_h1 = True
                contact_lines_remaining = 2
            i += 1
            continue

        project_group = parse_project_group(line)
        if project_group:
            close_lists()
            label, title, intro = project_group
            title_html = inline_markdown(title)
            if intro:
                intro_html = inline_markdown(intro)
                output.append(
                    '<p class="project-group">'
                    f'<strong>{html.escape(label)}：{title_html}</strong>'
                    f'<span class="project-intro-inline">：{intro_html}</span></p>'
                )
            else:
                output.append(
                    f'<p class="project-group"><strong>{html.escape(label)}：{title_html}</strong></p>'
                )
            i += 1
            continue

        bold_project = parse_bold_project_header(line)
        if bold_project and current_section == "实习经历":
            close_lists()
            output.append(
                f'<p class="project-group"><strong>{inline_markdown(bold_project)}</strong></p>'
            )
            i += 1
            if i < len(lines):
                next_line = lines[i].strip()
                if (
                    next_line
                    and not match_sub_item(next_line)
                    and not is_bold_project_header(next_line)
                    and not parse_project_group(next_line)
                    and not re.match(r"^(\d+)\.\s+", next_line)
                    and not (
                        next_line.startswith("**")
                        and re.search(rf"\d{{4}}\.\d{{2}}|{DATE_END_PATTERN}", next_line)
                    )
                    and not match_project_task(next_line)
                ):
                    output.append(f'<p class="project-intro">{inline_markdown(next_line)}</p>')
                    i += 1
            continue

        bullet_task = BULLET_TASK_RE.match(line)
        if bullet_task:
            close_lists()
            item_html, i = collect_list_item_text(bullet_task.group(1), i + 1)
            output.append(f'<p class="project-task">{item_html}</p>')
            continue

        project_task = match_project_task(line)
        if project_task and current_section == "实习经历":
            close_lists()
            item_html, i = collect_list_item_text(line, i + 1)
            output.append(f'<p class="project-task">{item_html}</p>')
            continue

        sub_item = match_sub_item(line)
        if sub_item:
            close_lists()
            item_html, i = collect_list_item_text(sub_item.group(2), i + 1)
            output.append(
                f'<p class="project-task">{html.escape(sub_item.group(1))}）{item_html}</p>'
            )
            continue

        unordered = re.match(r"^[-*]\s+(.+)$", line)
        if unordered:
            if in_ol:
                output.append("</ol>")
                in_ol = False
            if not in_ul:
                output.append("<ul>")
                in_ul = True
            item_html, i = collect_list_item_text(unordered.group(1), i + 1)
            output.append(f"<li>{item_html}</li>")
            continue

        ordered = re.match(r"^(\d+)\.\s+(.+)$", line)
        if ordered:
            if in_ul:
                output.append("</ul>")
                in_ul = False
            if not in_ol:
                output.append("<ol>")
                in_ol = True
            # Bake "N. " into text: Chromium print often drops CSS list markers,
            # and body > ol uses list-style:none (skills / top-level ordered items).
            num = int(ordered.group(1))
            item_html, i = collect_list_item_text(ordered.group(2), i + 1)
            output.append(f'<li value="{num}">{num}. {item_html}</li>')
            continue

        close_lists()
        if seen_h1 and current_section is None and re.search(r"(?:@|\d{7,})", line):
            contact_lines_remaining = 0
            output.append(f'<p class="contact">{inline_markdown(line)}</p>')
            i += 1
            continue
        if seen_h1 and current_section is None and re.match(
            r"^(?:应聘|Applying for|Target Role|Target)[：:]",
            line.strip(),
            flags=re.I,
        ):
            contact_lines_remaining = 0
            output.append(f'<p class="contact">{inline_markdown(line)}</p>')
            i += 1
            continue
        if seen_h1 and current_section is None and re.fullmatch(r"\*\*[^*]+\*\*", line.strip()):
            contact_lines_remaining = 0
            output.append(f'<p class="contact">{inline_markdown(line)}</p>')
            i += 1
            continue
        if contact_lines_remaining > 0:
            contact_parts = [inline_markdown(line)]
            consumed = 1
            next_index = i + 1
            while consumed < contact_lines_remaining and next_index < len(lines):
                next_raw = lines[next_index]
                next_line = next_raw.strip()
                if not next_line:
                    break
                if (
                    ("|" in next_line and next_index + 1 < len(lines) and is_table_separator(lines[next_index + 1]))
                    or re.fullmatch(r"-{3,}|\*{3,}|_{3,}", next_line)
                    or re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", next_line)
                    or re.match(r"^(#{1,3})\s+(.+)$", next_line)
                    or re.match(r"^[-*]\s+(.+)$", next_line)
                    or re.match(r"^(\d+)\.\s+(.+)$", next_line)
                    or match_sub_item(next_line)
                    or parse_project_group(next_line)
                    or is_bold_project_header(next_line)
                    or is_project_task_line(next_line)
                ):
                    break
                contact_parts.append(inline_markdown(next_line))
                consumed += 1
                next_index += 1
            contact_lines_remaining = max(0, contact_lines_remaining - consumed)
            output.append(f'<p class="contact">{"<br>".join(contact_parts)}</p>')
            i = next_index
            continue

        is_grid_heading = current_section in {"教育经历", "实习经历", "项目经历"} and bool(
            re.match(rf"^\*\*[^*]+\*\*\s+.+(?:\d{{4}}\.\d{{2}}|{DATE_END_PATTERN})", line)
        )
        row_heading_html = (
            render_row_heading(line, "，,") if current_section == "教育经历" and is_grid_heading
            else render_row_heading(line) if is_grid_heading
            else None
        )
        if row_heading_html:
            output.append(row_heading_html)
            i += 1
            continue
        css_class = ' class="row-heading"' if is_grid_heading else ""
        output.append(f"<p{css_class}>{inline_markdown(line)}</p>")
        i += 1

    close_lists()
    return "\n".join(output)


def is_english_resume(markdown_text: str) -> bool:
    """Detect English resumes so PDF can use Times New Roman without affecting Chinese layouts."""
    if re.search(r"(?m)^##\s+(教育经历|实习经历|相关技能)\s*$", markdown_text):
        return False
    if re.search(r"(?im)^Applying for\s*:", markdown_text):
        return True
    if re.search(r"(?m)^##\s+(Education|Experience|Skills|Relevant Skills)\s*$", markdown_text):
        return True
    return False


def build_html(markdown_text: str, preset_name: str, base_dir: Path) -> str:
    preset = PRESETS[preset_name]
    photo_width = preset.get("photo_width", "58pt")
    photo_height = preset.get("photo_height", "85pt")
    margin_top = preset.get("margin_top", "1.0cm")
    margin_x = preset.get("margin_x", "2.0cm")
    h2_font_size = preset.get("h2_font_size", "11pt")
    project_group_margin_top = preset.get("project_group_margin_top", "4pt")
    project_group_margin_after = preset.get("project_group_margin_after", "1.5pt")
    project_intro_font_size = preset.get("project_intro_font_size", "8.6pt")
    project_intro_margin_after = preset.get("project_intro_margin_after", "2pt")
    company_gap_after_task = preset.get("company_gap_after_task", "5pt")
    name_font_size = preset.get("name_font_size", "17pt")
    contact_font_size = preset.get("contact_font_size", "10pt")
    row_heading_font_size = preset.get("row_heading_font_size", "10.8pt")
    skill_item_margin_after = preset.get("skill_item_margin_after", "2pt")
    body = markdown_to_body(markdown_text, base_dir)
    english = is_english_resume(markdown_text)
    html_lang = "en" if english else "zh-CN"
    font_family = (
        '"Times New Roman", Times, serif'
        if english
        else '"Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "SimSun", sans-serif'
    )
    # English-only softer layout: keep Times New Roman, ease visual sharpness
    # without changing Chinese resume CSS.
    if english:
        body_color = "#222222"
        body_font_size = preset.get("body_font_size", "9.5pt")
        # Softer than ZH default (1.3) / compact (1.22), but still fit one page.
        body_line_height = {
            "standard": "1.30",
            "fill": "1.30",
            "tight": "1.28",
            "compact": "1.26",
            "onepage_dense": "1.20",
        }.get(preset_name, "1.30")
        task_line_height = body_line_height
        h2_padding = "2pt 0 2pt 5pt"
        h2_border_left = "1.25pt solid #6A6A6A"
        h2_background = "#F5F5F5"
        h2_color = "#2A2A2A"
        h2_margin_top = "7pt" if preset_name != "onepage_dense" else preset.get("h2_margin_top", "4pt")
        project_intro_color = "#6E6E6E"
        task_margin_after = preset.get("task_margin_after", "4pt")
        text_justify = "auto"
        letter_spacing = "0.01em"
    else:
        # 默认中文样式对齐「定稿中文一页简历样式」：灰底左竖条分区、姓名下划线、
        # 项目简介左灰条斜体；相关技能不加行间横线。
        body_color = "#1a1a1a"
        body_font_size = preset.get("body_font_size", "9.5pt")
        body_line_height = preset["line_height"]
        task_line_height = preset["line_height"]
        h2_padding = "1.5pt 0 1.5pt 6pt"
        h2_border_left = "2.5pt solid #2C2C2C"
        h2_background = "#F0F0F0"
        h2_color = "#1A1A1A"
        h2_margin_top = preset.get("h2_margin_top", "5pt")
        project_intro_color = "#666666"
        task_margin_after = preset.get("task_margin_after", "3.5pt")
        text_justify = "inter-ideograph"
        letter_spacing = "normal"
    return f"""<!doctype html>
<html lang="{html_lang}">
<head>
  <meta charset="utf-8">
  <title>Resume</title>
  <style>
    @page {{
      size: A4;
      margin: {margin_top} {margin_x} {preset["margin_bottom"]} {margin_x};
    }}
    * {{
      box-sizing: border-box;
    }}
    html, body {{
      margin: 0;
      padding: 0;
    }}
    body {{
      color: {body_color};
      font-family: {font_family};
      font-size: {body_font_size};
      line-height: {body_line_height};
      letter-spacing: {letter_spacing};
      padding-top: {preset["body_padding_top"]};
      position: relative;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    h1 {{
      margin: 0 0 3pt;
      padding-bottom: 4pt;
      text-align: center;
      font-size: {name_font_size};
      line-height: {FIXED_LINE_HEIGHT};
      font-weight: 700;
      letter-spacing: 4pt;
      border-bottom: 1.2pt solid #2c2c2c;
    }}
    .contact {{
      margin: 3pt 0 0;
      text-align: center;
      text-align-last: center;
      font-size: {contact_font_size};
      line-height: {FIXED_LINE_HEIGHT};
      color: #555;
      letter-spacing: 0.2pt;
    }}
    .row-heading {{
      margin: 0 0 2pt;
      font-size: {row_heading_font_size};
      line-height: {body_line_height};
      font-weight: 700;
    }}
    .row-heading-grid {{
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      column-gap: 6pt;
      align-items: baseline;
      width: 100%;
      white-space: normal;
      margin: 0 0 1pt;
    }}
    .row-company {{
      grid-column: 1;
      justify-self: start;
      text-align: left;
      font-weight: 700;
      padding-right: 4pt;
    }}
    .row-role {{
      grid-column: 2;
      justify-self: center;
      text-align: center;
      white-space: nowrap;
      font-weight: 400;
      color: #444;
      padding: 0 4pt;
    }}
    .row-date {{
      grid-column: 3;
      justify-self: end;
      text-align: right;
      white-space: nowrap;
      font-weight: 400;
      color: #555;
      font-variant-numeric: tabular-nums;
    }}
    .photo {{
      position: absolute;
      top: 0;
      right: 0;
      margin: 0;
      width: {photo_width};
      height: {photo_height};
      min-width: {photo_width};
      max-width: {photo_width};
      min-height: {photo_height};
      max-height: {photo_height};
      text-align: right;
      overflow: visible;
    }}
    .photo img {{
      display: block;
      width: {photo_width};
      height: {photo_height};
      min-width: {photo_width};
      max-width: {photo_width};
      min-height: {photo_height};
      max-height: {photo_height};
      object-fit: contain;
      object-position: center center;
      background: #fff;
      border: none;
    }}
    h2 {{
      margin: {h2_margin_top} 0 {preset["section_margin_after"]};
      padding: {h2_padding};
      border-bottom: 0;
      border-left: {h2_border_left};
      background: {h2_background};
      font-size: {h2_font_size};
      line-height: 1.2;
      font-weight: 700;
      letter-spacing: 0.8pt;
      color: {h2_color};
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    h3 {{
      margin: 4pt 0 2pt;
      font-size: {h2_font_size};
      line-height: {FIXED_LINE_HEIGHT};
      font-weight: 700;
    }}
    p.project-group {{
      margin: {project_group_margin_top} 0 {project_group_margin_after};
      line-height: {FIXED_LINE_HEIGHT};
    }}
    p.project-group + p.project-task {{
      margin-top: 0;
    }}
    p.project-task + p.project-group {{
      margin-top: {project_group_margin_top};
    }}
    p.project-group strong {{
      font-weight: 700;
    }}
    span.project-intro-inline {{
      font-weight: 400;
      color: {project_intro_color};
      font-style: italic;
    }}
    p.project-intro {{
      margin: 0 0 {project_intro_margin_after};
      padding: 0 0 0 10pt;
      border-left: 1.2pt solid #d8d8d8;
      line-height: {FIXED_LINE_HEIGHT};
      font-size: {project_intro_font_size};
      font-weight: 400;
      color: {project_intro_color};
      font-style: italic;
      text-align: justify;
      text-align-last: left;
      text-justify: {text_justify};
    }}
    p.project-intro strong {{
      font-style: italic;
      font-weight: 700;
      color: {body_color};
    }}
    p.project-group + p.project-intro {{
      margin-top: 0;
    }}
    p.project-intro + p.project-task {{
      margin-top: 0.5pt;
    }}
    p.project-task {{
      margin: 0 0 {task_margin_after};
      padding-left: 10pt;
      text-indent: 0;
      line-height: {task_line_height};
      text-align: justify;
      text-align-last: left;
      text-justify: {text_justify};
    }}
    p.project-task::before {{
      content: none;
    }}
    p.project-task + p.project-group {{
      margin-top: {project_group_margin_top};
    }}
    p.project-task + .row-heading-grid {{
      margin-top: {company_gap_after_task};
    }}
    p.row-heading-grid + p.project-group {{
      margin-top: 2pt;
    }}
    .row-heading-grid + p:not(.row-heading-grid):not(.project-group):not(.project-task):not(.project-intro) {{
      color: #555;
      font-size: 8.8pt;
      margin: 0 0 4pt 0;
    }}
    span.task-num {{
      font-weight: 400;
    }}
    p {{
      margin: 0 0 {preset["paragraph_margin_after"]};
      line-height: {body_line_height};
      white-space: pre-wrap;
      text-align: justify;
      text-align-last: left;
      text-justify: {text_justify};
    }}
    ul, ol {{
      margin: 0 0 {preset["paragraph_margin_after"]} 0;
      padding-left: 0;
      list-style-position: inside;
    }}
    body > ol {{
      margin-top: 1pt;
      padding-left: 0;
      list-style: none;
    }}
    body > ol li {{
      margin: 0 0 {skill_item_margin_after} 0;
      padding: 0.5pt 0 0.5pt 10pt;
      border-bottom: none;
      line-height: {task_line_height};
      text-align: justify;
      text-align-last: left;
      text-justify: {text_justify};
    }}
    body > ol li:last-child {{
      border-bottom: none;
      margin-bottom: 0;
    }}
    li {{
      margin: 0 0 {preset["paragraph_margin_after"]};
      padding-left: 0;
      line-height: {task_line_height};
      text-align: justify;
      text-align-last: left;
      text-justify: {text_justify};
    }}
    hr {{
      border: 0;
      height: 0;
      margin: 2pt 0 0;
      border-top: 0;
      display: none;
    }}
    hr + h2 {{
      margin-top: {h2_margin_top};
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 0 0 {preset["paragraph_margin_after"]};
      font-size: 9.5pt;
      line-height: {FIXED_LINE_HEIGHT};
    }}
    th, td {{
      border: 1px solid #ddd;
      padding: 2pt 4pt;
      text-align: left;
      vertical-align: top;
    }}
    strong {{
      font-weight: 700;
      color: #000;
    }}
    code {{
      font-family: inherit;
      background: transparent;
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def find_browser(explicit_path: Path | None) -> Path:
    if explicit_path:
        if explicit_path.exists():
            return explicit_path
        raise FileNotFoundError(f"Browser path does not exist: {explicit_path}")

    command_names = ["msedge", "chrome", "chromium", "google-chrome", "chrome.exe", "msedge.exe"]
    for name in command_names:
        found = shutil.which(name)
        if found:
            return Path(found)

    candidates = [
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "Could not find Microsoft Edge, Chrome, or Chromium. Install one or pass --browser."
    )


def print_pdf(browser: Path, html_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="resume_browser_", ignore_cleanup_errors=True
    ) as profile_dir, tempfile.TemporaryDirectory(
        prefix="resume_pdf_out_", ignore_cleanup_errors=True
    ) as output_dir:
        temp_pdf = Path(output_dir) / "output.pdf"
        command = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={profile_dir}",
            "--no-pdf-header-footer",
            f"--print-to-pdf={temp_pdf}",
            html_path.resolve().as_uri(),
        ]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode != 0:
            fallback = command.copy()
            fallback[1] = "--headless"
            result = subprocess.run(
                fallback,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
        if result.returncode != 0:
            message = (result.stderr or result.stdout or "").strip()
            raise RuntimeError(f"Browser PDF export failed. {message}")
        for _ in range(40):
            if temp_pdf.exists():
                break
            time.sleep(0.25)
        if not temp_pdf.exists():
            message = (result.stderr or result.stdout or "").strip()
            raise RuntimeError(f"Browser PDF export did not create output.pdf. {message}")
        shutil.copyfile(temp_pdf, pdf_path)


def main() -> int:
    args = parse_args()
    input_path = args.input
    if not input_path.exists():
        print(f"Input Markdown not found: {input_path}", file=sys.stderr)
        return 1

    markdown_text = input_path.read_text(encoding="utf-8")
    output_path = args.output or default_output_path(input_path, markdown_text)
    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path
    validation_errors = validate_resume_markdown(
        markdown_text,
        input_path.parent,
        output_path,
    )
    if validation_errors:
        print("Error: resume Markdown does not meet resume-tailor SKILL requirements.", file=sys.stderr)
        for error in validation_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    rendered_html = build_html(markdown_text, args.preset, input_path.parent)
    browser = find_browser(args.browser)

    if args.keep_html:
        html_path = output_path.with_suffix(".html")
        html_path.write_text(rendered_html, encoding="utf-8")
        print_pdf(browser, html_path, output_path)
    else:
        with tempfile.TemporaryDirectory(prefix="resume_pdf_") as tmpdir:
            html_path = Path(tmpdir) / "resume.html"
            html_path.write_text(rendered_html, encoding="utf-8")
            print_pdf(browser, html_path, output_path)

    page_count = count_pdf_pages(output_path)
    if page_count != 1:
        if args.allow_multipage:
            print(f"PDF written: {output_path}")
            print(f"Page check: {page_count} pages.")
            print("Skill check: skipped for multipage preview.")
            return 0
        output_path.unlink(missing_ok=True)
        print(
            f"Error: exported PDF has {page_count} pages, but this resume must be exactly 1 page.",
            file=sys.stderr,
        )
        print(
            "Use --preset tight for overflow, --preset fill for sparse content, or edit the Markdown length.",
            file=sys.stderr,
        )
        return 2

    layout_errors, bottom_gap_mm = validate_pdf_layout(output_path)
    if layout_errors:
        output_path.unlink(missing_ok=True)
        print("Error: exported PDF does not meet resume-tailor SKILL layout requirements.", file=sys.stderr)
        for error in layout_errors:
            print(f"- {error}", file=sys.stderr)
        print(
            "Use --preset fill, enrich truthful JD-matched content, or adjust the Markdown length.",
            file=sys.stderr,
        )
        return 3

    print(f"PDF written: {output_path}")
    print("Page check: 1 page.")
    if bottom_gap_mm is not None:
        print(f"Bottom whitespace check: {bottom_gap_mm:.1f}mm.")
    print("Skill check: passed.")
    print("Tip: use --preset fill if the bottom is too empty; --preset tight/compact/onepage_dense if it overflows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

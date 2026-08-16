#!/usr/bin/env python3
"""
Check machine-verifiable resume format and PDF layout rules.

This script does not validate resume content quality, truthfulness, JD relevance,
or evidence selection. Those checks must be performed manually by the Agent.
It does validate machine-checkable photo rules: the Markdown must include one
workspace-local headshot and the exported PDF photo must not overlap text.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import markdown_resume_to_pdf as exporter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate machine-checkable resume Markdown/PDF format and layout rules."
    )
    parser.add_argument("input", type=Path, help="Input Markdown resume path.")
    parser.add_argument(
        "--pdf",
        type=Path,
        help="Optional exported PDF path. Defaults to the inferred 公司+姓名+岗位.pdf path.",
    )
    parser.add_argument(
        "--markdown-only",
        action="store_true",
        help="Only validate machine-checkable Markdown format rules; skip PDF page and bottom whitespace checks.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = args.input
    if not input_path.exists():
        print(f"Error: input Markdown not found: {input_path}", file=sys.stderr)
        return 1

    markdown_text = input_path.read_text(encoding="utf-8")
    pdf_path = args.pdf or exporter.default_output_path(input_path, markdown_text)
    if not pdf_path.is_absolute():
        pdf_path = Path.cwd() / pdf_path

    errors = exporter.validate_resume_markdown(
        markdown_text,
        input_path.parent,
        pdf_path,
    )

    if not args.markdown_only:
        if not pdf_path.exists():
            errors.append(f"Exported PDF not found: {pdf_path}")
        else:
            page_count = exporter.count_pdf_pages(pdf_path)
            if page_count != 1:
                errors.append(
                    f"PDF page count must be exactly 1; current page count is {page_count}."
                )
            layout_errors, bottom_gap_mm = exporter.validate_pdf_layout(pdf_path)
            errors.extend(layout_errors)

    if errors:
        print("Skill check: failed.")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Markdown check: passed.")
    if not args.markdown_only:
        print("Page check: 1 page.")
        _, bottom_gap_mm = exporter.validate_pdf_layout(pdf_path)
        if bottom_gap_mm is not None:
            print(f"Bottom whitespace check: {bottom_gap_mm:.1f}mm.")
    print("Skill check: passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

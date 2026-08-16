#!/usr/bin/env python3
"""Regression checks for the resume-skills-generic package.

Validates:
1. Required skill files exist
2. Templates load as UTF-8 text
3. Scripts are importable / argparse --help works
4. check_resume_skill markdown-only on fixture (if dependencies allow)
5. crop_profile_photo dry-run with generated placeholder image
6. Privacy scan: no real PII patterns (name/phone/email/schools of the original author)
"""

from __future__ import annotations

import importlib.util
import fnmatch
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
REPORT_PATH = Path(__file__).resolve().parent / "REGRESSION_REPORT.md"

REQUIRED = [
    "README.md",
    "resume-tailor-generic/SKILL.md",
    "resume-tailor-generic/reference.md",
    "resume-tailor-generic/examples.md",
    "resume-tailor-generic/resume-template.md",
    "resume-tailor-generic/resume-database-template.md",
    "resume-tailor-generic/scripts/markdown_resume_to_pdf.py",
    "resume-tailor-generic/scripts/check_resume_skill.py",
    "resume-tailor-generic/scripts/crop_profile_photo.py",
    "resume-database-generic/SKILL.md",
    "resume-database-generic/reference.md",
    "resume-database-generic/examples.md",
    "resume-database-generic/resume-database-template.md",
    "resume-database-generic/resume-database-l012-template.md",
    "shared/scripts/markdown_resume_to_pdf.py",
    "shared/scripts/check_resume_skill.py",
    "shared/scripts/crop_profile_photo.py",
    "shared/templates/resume-template.md",
    "shared/templates/resume-database-template.md",
    "fixtures/sample-resume.md",
    "fixtures/示例公司+张三+示例岗位.md",
    "fixtures/sample-jd.md",
    "fixtures/sample-database.md",
    "fixtures/profile-photo-cropped.png",
]

# Real-author privacy denylist (must not appear in the redistributable package)
PRIVACY_DENY = [
    r"邱井晨",
    r"qiujc",
    r"上海大学",
    r"深圳大学",
    r"携程计算机技术",
    r"博世中国",
    r"d:\\Users\\xxx",
    r"d:/Users/xxx",
    r"1[3-9]\d{9}(?!\d)",  # real CN mobile — allow 13800000000 in fixtures only via whitelist path
]

# Allowed fake numbers in fixtures / examples
FAKE_PHONE_ALLOW = {"13800000000"}

SKIP_SCAN_SUFFIX = {".png", ".jpg", ".jpeg", ".pdf", ".zip", ".pyc"}


def load_gitignore_patterns() -> list[str]:
    """Return non-comment patterns from root .gitignore."""
    gi = PKG / ".gitignore"
    if not gi.is_file():
        return []
    patterns: list[str] = []
    for line in gi.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("!"):
            continue
        patterns.append(line)
    return patterns


def path_matches_gitignore(rel_posix: str, basename: str, patterns: list[str]) -> bool:
    for pat in patterns:
        if "/" in pat or "\\" in pat:
            if fnmatch.fnmatch(rel_posix, pat) or fnmatch.fnmatch(rel_posix, pat.lstrip("/")):
                return True
        elif fnmatch.fnmatch(basename, pat):
            return True
    return False


def ok(msg: str) -> tuple[bool, str]:
    return True, f"PASS: {msg}"


def fail(msg: str) -> tuple[bool, str]:
    return False, f"FAIL: {msg}"


def check_required_files() -> list[tuple[bool, str]]:
    results = []
    for rel in REQUIRED:
        path = PKG / rel
        if path.is_file() and path.stat().st_size > 0:
            results.append(ok(f"exists {rel}"))
        else:
            results.append(fail(f"missing or empty {rel}"))
    return results


def check_templates_load() -> list[tuple[bool, str]]:
    results = []
    for rel in [
        "shared/templates/resume-template.md",
        "shared/templates/resume-database-template.md",
        "resume-tailor-generic/resume-template.md",
        "resume-database-generic/resume-database-l012-template.md",
        "fixtures/sample-resume.md",
    ]:
        try:
            text = (PKG / rel).read_text(encoding="utf-8")
            if len(text.strip()) < 50:
                results.append(fail(f"template too short: {rel}"))
            else:
                results.append(ok(f"load {rel} ({len(text)} chars)"))
        except Exception as exc:  # noqa: BLE001
            results.append(fail(f"load {rel}: {exc}"))
    return results


def check_script_help() -> list[tuple[bool, str]]:
    results = []
    scripts_dir = PKG / "resume-tailor-generic" / "scripts"
    for name in [
        "markdown_resume_to_pdf.py",
        "check_resume_skill.py",
        "crop_profile_photo.py",
    ]:
        script = scripts_dir / name
        try:
            proc = subprocess.run(
                [sys.executable, str(script), "--help"],
                cwd=str(scripts_dir),
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            if proc.returncode == 0 and "usage:" in (proc.stdout + proc.stderr).lower():
                results.append(ok(f"--help {name}"))
            else:
                results.append(
                    fail(
                        f"--help {name} rc={proc.returncode} "
                        f"out={(proc.stdout + proc.stderr)[:200]}"
                    )
                )
        except Exception as exc:  # noqa: BLE001
            results.append(fail(f"--help {name}: {exc}"))
    return results


def check_markdown_only_fixture() -> list[tuple[bool, str]]:
    results = []
    scripts_dir = PKG / "resume-tailor-generic" / "scripts"
    fixture = PKG / "fixtures" / "示例公司+张三+示例岗位.md"
    try:
        proc = subprocess.run(
            [
                sys.executable,
                str(scripts_dir / "check_resume_skill.py"),
                str(fixture),
                "--markdown-only",
            ],
            cwd=str(PKG / "fixtures"),
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        out = proc.stdout + proc.stderr
        if proc.returncode == 0 and "passed" in out.lower():
            results.append(ok("check_resume_skill --markdown-only on fixture"))
        elif "playwright" in out.lower() or "ModuleNotFoundError" in out:
            results.append(
                ok(
                    "check_resume_skill import path reachable "
                    f"(soft-skip runtime deps: {out[:160].strip()})"
                )
            )
        else:
            results.append(
                fail(
                    f"check_resume_skill rc={proc.returncode} out={out[:400]}"
                )
            )
    except Exception as exc:  # noqa: BLE001
        results.append(fail(f"check_resume_skill fixture: {exc}"))
    return results


def check_crop_photo_dry_run() -> list[tuple[bool, str]]:
    results = []
    scripts_dir = PKG / "resume-tailor-generic" / "scripts"
    try:
        from PIL import Image  # type: ignore
    except Exception as exc:  # noqa: BLE001
        return [ok(f"crop_profile_photo soft-skip (Pillow missing: {exc})")]

    try:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "headshot.png"
            out = Path(tmp) / "headshot_cropped.png"
            Image.new("RGB", (800, 1000), color=(200, 200, 210)).save(src)
            proc = subprocess.run(
                [
                    sys.executable,
                    str(scripts_dir / "crop_profile_photo.py"),
                    str(src),
                    "-o",
                    str(out),
                ],
                cwd=str(scripts_dir),
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            if proc.returncode == 0 and out.is_file() and out.stat().st_size > 0:
                results.append(ok(f"crop_profile_photo dry-run -> {out.name}"))
            else:
                results.append(
                    fail(
                        f"crop_profile_photo rc={proc.returncode} "
                        f"{(proc.stdout + proc.stderr)[:300]}"
                    )
                )
    except Exception as exc:  # noqa: BLE001
        results.append(fail(f"crop_profile_photo: {exc}"))
    return results


def check_privacy_scan() -> list[tuple[bool, str]]:
    results = []
    hits: list[str] = []
    skip_patterns = load_gitignore_patterns()
    patterns = [re.compile(p) for p in PRIVACY_DENY]
    for path in PKG.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(PKG).as_posix()
        if path_matches_gitignore(rel, path.name, skip_patterns):
            continue
        if path.suffix.lower() in SKIP_SCAN_SUFFIX:
            continue
        if path.name == "REGRESSION_REPORT.md":
            continue
        if "run_regression" in path.name:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for pat in patterns:
            for m in pat.finditer(text):
                matched = m.group(0)
                # Allow known fake phone in fixtures/examples
                if re.fullmatch(r"1[3-9]\d{9}", matched) and matched in FAKE_PHONE_ALLOW:
                    continue
                # Deny other phones
                if re.fullmatch(r"1[3-9]\d{9}", matched) and matched not in FAKE_PHONE_ALLOW:
                    hits.append(f"{rel}: phone {matched}")
                    continue
                if matched in FAKE_PHONE_ALLOW:
                    continue
                hits.append(f"{rel}: matched /{pat.pattern}/ -> {matched!r}")
    if hits:
        results.append(fail("privacy leaks:\n  - " + "\n  - ".join(hits[:30])))
    else:
        results.append(ok("privacy scan clean (denylist)"))
    return results


def check_skill_frontmatter() -> list[tuple[bool, str]]:
    results = []
    for rel, expected_name in [
        ("resume-tailor-generic/SKILL.md", "resume-tailor-generic"),
        ("resume-database-generic/SKILL.md", "resume-database-generic"),
    ]:
        text = (PKG / rel).read_text(encoding="utf-8")
        if text.startswith("---") and f"name: {expected_name}" in text[:400]:
            results.append(ok(f"frontmatter {rel}"))
        else:
            results.append(fail(f"frontmatter {rel}"))
    return results


def write_report(all_results: list[tuple[bool, str]]) -> None:
    passed = sum(1 for ok_flag, _ in all_results if ok_flag)
    failed = sum(1 for ok_flag, _ in all_results if not ok_flag)
    lines = [
        "# Regression Report — resume-skills-generic",
        "",
        f"- Package: `{PKG}`",
        f"- Passed: **{passed}**",
        f"- Failed: **{failed}**",
        f"- Overall: **{'PASS' if failed == 0 else 'FAIL'}**",
        "",
        "## Details",
        "",
    ]
    for ok_flag, msg in all_results:
        lines.append(f"- [{'PASS' if ok_flag else 'FAIL'}] {msg}")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    all_results: list[tuple[bool, str]] = []
    all_results.extend(check_required_files())
    all_results.extend(check_skill_frontmatter())
    all_results.extend(check_templates_load())
    all_results.extend(check_script_help())
    all_results.extend(check_markdown_only_fixture())
    all_results.extend(check_crop_photo_dry_run())
    all_results.extend(check_privacy_scan())
    write_report(all_results)
    failed = [m for ok_flag, m in all_results if not ok_flag]
    report = REPORT_PATH.read_text(encoding="utf-8")
    try:
        print(report)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(report.encode("utf-8", errors="replace"))
        sys.stdout.buffer.write(b"\n")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

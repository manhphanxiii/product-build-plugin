#!/usr/bin/env python3
"""Validate shared skill blocks and dual-host plugin invariants."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


FIRST_PARTY = (
    "evals-gate",
    "idea-to-product-concept",
    "implement",
    "prototype",
    "review-code",
    "start-repo",
    "to-prd",
    "to-ticket",
    "update",
)
REVIEW_SKILLS = (
    "evals-gate",
    "idea-to-product-concept",
    "prototype",
    "to-prd",
    "to-ticket",
    "update",
)
STANDARD_ROOT_SKILLS = (
    "evals-gate",
    "idea-to-product-concept",
    "implement",
    "prototype",
    "to-prd",
    "to-ticket",
)
SHARED_MANIFEST_FIELDS = (
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
)


def extract_section(text: str, heading: str) -> str | None:
    marker = f"{heading}\n"
    start = text.find(marker)
    if start < 0:
        return None
    search_from = start + len(marker)
    match = re.search(r"^## ", text[search_from:], flags=re.MULTILINE)
    end = len(text) if match is None else search_from + match.start()
    return text[start:end].rstrip() + "\n"


def extract_block(text: str, heading: str, terminal_line: str) -> str | None:
    marker = f"{heading}\n"
    start = text.find(marker)
    if start < 0:
        return None
    terminal_start = text.find(terminal_line, start + len(marker))
    if terminal_start < 0:
        return None
    end = terminal_start + len(terminal_line)
    return text[start:end].rstrip() + "\n"


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc
    values: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.fullmatch(r"([A-Za-z0-9_-]+):\s*(.*?)\s*", line)
        if match:
            values[match.group(1)] = match.group(2).strip('"\'')
    return values


def read_json(path: Path, errors: list[str]) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{path}: root must be an object")
        return {}
    return payload


def check_identical_sections(
    root: Path,
    skills: tuple[str, ...],
    heading: str,
    errors: list[str],
) -> None:
    baseline_name = skills[0]
    baseline_path = root / "skills" / baseline_name / "SKILL.md"
    baseline = extract_section(baseline_path.read_text(encoding="utf-8"), heading)
    if baseline is None:
        errors.append(f"{baseline_path}: missing {heading}")
        return
    for skill_name in skills[1:]:
        path = root / "skills" / skill_name / "SKILL.md"
        section = extract_section(path.read_text(encoding="utf-8"), heading)
        if section is None:
            errors.append(f"{path}: missing {heading}")
        elif section != baseline:
            errors.append(f"{path}: {heading} differs from {baseline_path}")


def check_identical_blocks(
    root: Path,
    skills: tuple[str, ...],
    heading: str,
    terminal_line: str,
    errors: list[str],
) -> None:
    baseline_name = skills[0]
    baseline_path = root / "skills" / baseline_name / "SKILL.md"
    baseline = extract_block(
        baseline_path.read_text(encoding="utf-8"), heading, terminal_line
    )
    if baseline is None:
        errors.append(f"{baseline_path}: missing or incomplete {heading}")
        return
    for skill_name in skills[1:]:
        path = root / "skills" / skill_name / "SKILL.md"
        block = extract_block(path.read_text(encoding="utf-8"), heading, terminal_line)
        if block is None:
            errors.append(f"{path}: missing or incomplete {heading}")
        elif block != baseline:
            errors.append(f"{path}: {heading} differs from {baseline_path}")


def check_plan_gate(root: Path, errors: list[str]) -> None:
    path = root / "skills" / "start-repo" / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    heading = "## Plan gate"
    terminal_line = (
        "For an already initialized repository, include only missing files in the plan; "
        "when nothing is missing, execute nothing and direct the user to `/build:update`."
    )
    block = extract_block(text, heading, terminal_line)
    if block is None:
        errors.append(f"{path}: missing or incomplete {heading}")
        return

    gate_position = text.find(f"{heading}\n")
    for phase in range(7, 11):
        marker = f"## Phase {phase}:"
        phase_position = text.find(marker)
        if phase_position < 0:
            errors.append(f"{path}: missing {marker}")
        elif phase_position < gate_position:
            errors.append(f"{path}: {marker} must appear after {heading}")


def check_skill_metadata(root: Path, errors: list[str]) -> None:
    skill_dirs = sorted(
        path.parent.name for path in (root / "skills").glob("*/SKILL.md")
    )
    if len(skill_dirs) != 10:
        errors.append(f"skills/: expected 10 skills, found {len(skill_dirs)}")
    for skill_name in skill_dirs:
        skill_path = root / "skills" / skill_name / "SKILL.md"
        try:
            frontmatter = parse_frontmatter(skill_path)
        except ValueError as exc:
            errors.append(f"{skill_path}: {exc}")
            continue
        if frontmatter.get("name") != skill_name:
            errors.append(
                f"{skill_path}: frontmatter name {frontmatter.get('name')!r} "
                f"does not match folder {skill_name!r}"
            )
        if not frontmatter.get("description"):
            errors.append(f"{skill_path}: description is required")

        openai_path = root / "skills" / skill_name / "agents" / "openai.yaml"
        if not openai_path.is_file():
            errors.append(f"{openai_path}: missing")
            continue
        openai_text = openai_path.read_text(encoding="utf-8")
        for field in ("display_name", "short_description"):
            if re.search(rf"^\s*{field}:\s*\S", openai_text, flags=re.MULTILINE) is None:
                errors.append(f"{openai_path}: interface.{field} is required")
        if frontmatter.get("disable-model-invocation") == "true":
            errors.append(
                f"{skill_path}: disable-model-invocation: true is rejected by the "
                "Codex universal plugin validator"
            )
        if skill_name == "start-repo" and re.search(
            r"^\s*allow_implicit_invocation:\s*false\s*$",
            openai_text,
            flags=re.MULTILINE,
        ) is None:
            errors.append(
                f"{openai_path}: start-repo must set allow_implicit_invocation: false"
            )


def check_manifests(root: Path, errors: list[str]) -> tuple[object, object]:
    claude_path = root / ".claude-plugin" / "plugin.json"
    codex_path = root / ".codex-plugin" / "plugin.json"
    claude = read_json(claude_path, errors)
    codex = read_json(codex_path, errors)
    for field in SHARED_MANIFEST_FIELDS:
        if claude.get(field) != codex.get(field):
            errors.append(f"plugin manifests: shared field {field!r} is not synchronized")
    if "skills" in claude:
        errors.append(f"{claude_path}: must not list skills individually")
    if codex.get("skills") != "./skills/":
        errors.append(f"{codex_path}: skills must be './skills/'")
    interface = codex.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"{codex_path}: interface object is required")
    else:
        required = (
            "displayName",
            "shortDescription",
            "longDescription",
            "developerName",
            "category",
            "capabilities",
            "defaultPrompt",
        )
        for field in required:
            if not interface.get(field):
                errors.append(f"{codex_path}: interface.{field} is required")
        if interface.get("displayName") != claude.get("displayName"):
            errors.append("plugin manifests: display names are not synchronized")
    return claude.get("version"), codex.get("version")


def check_readme_release_refs(
    root: Path,
    manifest_versions: tuple[object, object],
    errors: list[str],
) -> None:
    claude_version, codex_version = manifest_versions
    if not isinstance(claude_version, str) or claude_version != codex_version:
        return
    readme_path = root / "README.md"
    refs = sorted(
        set(
            re.findall(
                r"\bv\d+\.\d+\.\d+\b",
                readme_path.read_text(encoding="utf-8"),
            )
        )
    )
    expected = f"v{claude_version}"
    for ref in refs:
        if ref != expected:
            errors.append(
                f"{readme_path}: release ref {ref!r} must match manifest version {expected!r}"
            )


def check_release_tag(
    root: Path,
    manifest_versions: tuple[object, object],
    errors: list[str],
) -> None:
    claude_version, codex_version = manifest_versions
    if not isinstance(claude_version, str) or claude_version != codex_version:
        return
    tag = f"v{claude_version}"
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "ls-remote",
                "--exit-code",
                "--tags",
                "origin",
                f"refs/tags/{tag}",
            ],
            check=False,
            text=True,
            capture_output=True,
        )
    except OSError as exc:
        errors.append(f"release tag {tag!r}: could not run git: {exc}")
        return
    if result.returncode == 2:
        errors.append(f"release tag {tag!r} does not exist on origin")
    elif result.returncode != 0:
        detail = result.stderr.strip() or f"git exited with status {result.returncode}"
        errors.append(f"release tag {tag!r}: could not query origin: {detail}")


def check_portability(root: Path, errors: list[str]) -> None:
    forbidden_root_variable = "${" + "CLAUDE_PLUGIN_ROOT}"
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.parts[: len(root.parts)] != root.parts:
            continue
        relative = path.relative_to(root)
        if relative.parts[:2] == ("skills", "lavish"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if forbidden_root_variable in text:
            errors.append(f"{relative}: contains a Claude-specific plugin root variable")
        if "\u2013" in text or "\u2014" in text:
            errors.append(f"{relative}: contains an en dash or em dash")

    for skill_name in FIRST_PARTY:
        path = root / "skills" / skill_name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        for manifest_path in (
            ".claude-plugin/plugin.json",
            ".codex-plugin/plugin.json",
        ):
            if manifest_path not in text:
                errors.append(f"{path}: root guard does not mention {manifest_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root to validate",
    )
    parser.add_argument(
        "--release",
        action="store_true",
        help="Also require the manifest version tag to exist on origin",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    check_identical_blocks(
        root,
        FIRST_PARTY,
        "## Host resolution",
        "Use tools by capability, not by assumed host; when a named tool is unavailable, apply the fallback stated by the current phase and report the substitution in one line.",
        errors,
    )
    check_identical_blocks(
        root,
        REVIEW_SKILLS,
        "## Review gate",
        "Skip this gate only for genuinely unattended automation with no user available to approve a draft; a user-started asynchronous cloud run does not qualify.",
        errors,
    )
    check_plan_gate(root, errors)
    check_identical_sections(root, STANDARD_ROOT_SKILLS, "## Root resolution", errors)
    check_skill_metadata(root, errors)
    manifest_versions = check_manifests(root, errors)
    check_readme_release_refs(root, manifest_versions, errors)
    if args.release:
        check_release_tag(root, manifest_versions, errors)
    check_portability(root, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"check: failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("check: ok (10 skills, shared blocks, metadata, and dual-host manifests)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

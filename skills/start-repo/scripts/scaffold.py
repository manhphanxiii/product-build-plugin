#!/usr/bin/env python3
"""Scaffold a product-building workspace without overwriting existing files."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

BASE_FOLDER_READMES = {
    "app": "Sản phẩm thật, nơi code production chạy.",
    "client-note": "Tiếng nói khách hàng nguyên văn: sales call, support note và objection. Agent chỉ đọc, không sửa.",
    "demos": "Prototype throwaway và demo đã được thăng cấp để trình bày.",
    "routines": "Định nghĩa công việc lặp theo lịch, mỗi file ghi rõ cadence và output.",
    "report": "Output có ngày của routine; báo cáo chuỗi sản phẩm nằm trong report/product/.",
    "report/product": "Báo cáo có ngày do routine của chuỗi sản phẩm tạo ra.",
}

SEEDED_FILES = {
    "AGENTS.md": "AGENTS.md.template",
    "CLAUDE.md": "CLAUDE.md.template",
    "prd/evals/checklist.md": "checklist.md.template",
    "prd/README.md": "prd-README.md.template",
    "prd/roadmap.md": "roadmap.md.template",
    "routines/weekly-ops-review.md": "routines/weekly-ops-review.md",
    "routines/pr-auto-review.md": "routines/pr-auto-review.md",
}


def parse_links(values: list[str], root: Path, parser: argparse.ArgumentParser) -> dict[str, Path]:
    links: dict[str, Path] = {}
    for value in values:
        role, separator, raw_path = value.partition("=")
        role_path = Path(role)
        if not separator or not role or not raw_path:
            parser.error(f"--link phải có dạng ROLE=PATH, nhận được: {value!r}")
        if role_path.is_absolute() or ".." in role_path.parts or role_path == Path("."):
            parser.error(f"ROLE phải là đường dẫn tương đối bên trong repo: {role!r}")
        if role in links:
            parser.error(f"ROLE bị lặp trong --link: {role!r}")

        source = Path(raw_path).expanduser()
        if not source.is_absolute():
            source = root / source
        source = source.resolve()
        if not source.exists():
            parser.error(f"đích --link không tồn tại cho {role}: {source}")
        if not source.is_dir():
            parser.error(f"đích --link không phải thư mục cho {role}: {source}")
        links[role] = source
    return links


def is_under_link(path: str, linked_roles: set[str]) -> bool:
    parts = Path(path).parts
    return any(parts[: len(Path(role).parts)] == Path(role).parts for role in linked_roles)


def initialize_git(root: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0 and Path(result.stdout.strip()).resolve() == root:
        return False
    subprocess.run(
        ["git", "init", str(root)],
        capture_output=True,
        text=True,
        check=True,
    )
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="repo root")
    parser.add_argument("--retrofit", action="store_true", help="repo đã có code: không tạo nội dung trong app dir")
    parser.add_argument("--app-dir", default="app", help="tên thư mục code nếu khác app, ví dụ src")
    parser.add_argument("--link", action="append", default=[], metavar="ROLE=PATH", help="tạo symlink cho vai trò canonical")
    parser.add_argument("--no-knowledge-base", action="store_true", help="không tạo knowledge-base trong app dir")
    parser.add_argument("--init-git", action="store_true", help="git init nếu target chưa là một git repo riêng")
    args = parser.parse_args()

    root = Path(args.target).expanduser().resolve()
    if root.exists() and not root.is_dir():
        parser.error(f"repo root tồn tại nhưng không phải thư mục: {root}")
    links = parse_links(args.link, root, parser)

    root.mkdir(parents=True, exist_ok=True)
    git_initialized = initialize_git(root) if args.init_git else False
    created: list[str] = []
    skipped: list[str] = []
    created_links: list[tuple[str, Path]] = []

    for role, source in links.items():
        destination = root / role
        if os.path.lexists(destination):
            skipped.append(role)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            stored_target = os.path.relpath(source, start=destination.parent)
        except ValueError:
            stored_target = str(source)
        destination.symlink_to(stored_target, target_is_directory=True)
        created_links.append((role, source))

    folders = dict(BASE_FOLDER_READMES)
    app_blurb = folders.pop("app")
    if not args.retrofit:
        folders[args.app_dir] = app_blurb
    if not args.no_knowledge_base and not args.retrofit:
        folders[f"{args.app_dir}/knowledge-base"] = (
            "Kho kiến thức runtime của app. App đọc và ghi; agent chỉ đọc và không sửa tay nội dung tại đây."
        )

    for name, blurb in folders.items():
        if is_under_link(name, set(links)):
            continue
        directory = root / name
        directory.mkdir(parents=True, exist_ok=True)
        readme = directory / "README.md"
        relative = str(readme.relative_to(root))
        if os.path.lexists(readme):
            skipped.append(relative)
        else:
            readme.write_text(f"# /{name}\n\n{blurb}\n", encoding="utf-8")
            created.append(relative)

    for destination_name, template_name in SEEDED_FILES.items():
        if is_under_link(destination_name, set(links)):
            continue
        destination = root / destination_name
        source = ASSETS / template_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        if os.path.lexists(destination):
            skipped.append(destination_name)
            continue
        if not source.exists():
            print(f"!! thiếu template: {source}", file=sys.stderr)
            continue
        shutil.copyfile(source, destination)
        created.append(destination_name)

    print(f"Repo root: {root}\n")
    if git_initialized:
        print("Đã khởi tạo Git tại repo root.\n")
    print("Đã tạo:")
    for item in created:
        print(f"  + {item}")
    if skipped:
        print("\nBỏ qua (đã tồn tại, KHÔNG ghi đè):")
        for item in skipped:
            print(f"  = {item}")
    if created_links:
        print("\nSymlink đã tạo:")
        for role, source in created_links:
            print(f"  @ {role} -> {source}")
    print("\nBước tiếp: điền AGENTS.md trước, rồi CLAUDE.md, rồi prd/evals/checklist.md, rồi chạy /idea-to-product-concept.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

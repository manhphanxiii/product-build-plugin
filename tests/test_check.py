from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check.py"


class CheckScriptTests(unittest.TestCase):
    def copy_repo(self, temp_root: Path) -> Path:
        target = temp_root / "repo"
        shutil.copytree(
            REPO_ROOT,
            target,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
        return target

    def run_check(
        self, root: Path, *, release: bool = False
    ) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(CHECKER), "--root", str(root)]
        if release:
            command.append("--release")
        return subprocess.run(
            command,
            check=False,
            text=True,
            capture_output=True,
        )

    def manifest_version(self, root: Path) -> str:
        path = root / ".claude-plugin" / "plugin.json"
        return json.loads(path.read_text(encoding="utf-8"))["version"]

    def mutate_text(self, path: Path, old: str, new: str) -> None:
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def test_current_repository_passes(self) -> None:
        result = self.run_check(REPO_ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_each_invariant_has_a_negative_fixture(self) -> None:
        cases = (
            (
                "host block",
                lambda root: self.mutate_text(
                    root / "skills" / "implement" / "SKILL.md",
                    "Resolve the host once, before anything else",
                    "Resolve the current host once, before anything else",
                ),
            ),
            (
                "review block",
                lambda root: self.mutate_text(
                    root / "skills" / "prototype" / "SKILL.md",
                    "Choose the surface with this probe",
                    "Choose a surface with this probe",
                ),
            ),
            (
                "plan gate",
                lambda root: self.mutate_text(
                    root / "skills" / "start-repo" / "SKILL.md",
                    "## Plan gate\n\nAt the start",
                    "## Plan review\n\nAt the start",
                ),
            ),
            (
                "root block",
                lambda root: self.mutate_text(
                    root / "skills" / "implement" / "SKILL.md",
                    "Resolve `<root>` before reading or writing anything.",
                    "Resolve `<root>` before any read or write.",
                ),
            ),
            (
                "frontmatter name",
                lambda root: self.mutate_text(
                    root / "skills" / "implement" / "SKILL.md",
                    "name: implement",
                    "name: implementation",
                ),
            ),
            (
                "invocation policy",
                lambda root: self.mutate_text(
                    root / "skills" / "start-repo" / "agents" / "openai.yaml",
                    "allow_implicit_invocation: false",
                    "allow_implicit_invocation: true",
                ),
            ),
            (
                "manifest synchronization",
                lambda root: self.set_codex_version(root, "9.9.9"),
            ),
            (
                "README release ref",
                lambda root: self.mutate_text(
                    root / "README.md",
                    f"v{self.manifest_version(root)}",
                    "v9.9.9",
                ),
            ),
            (
                "Claude manifest skill list",
                lambda root: self.add_claude_skill_list(root),
            ),
            (
                "root guard",
                lambda root: self.mutate_text(
                    root / "skills" / "start-repo" / "SKILL.md",
                    ".codex-plugin/plugin.json",
                    ".codex-plugin/missing.json",
                ),
            ),
            (
                "host-specific root variable",
                lambda root: self.append_text(
                    root / "README.md",
                    "\n" + "${" + "CLAUDE_PLUGIN_ROOT}" + "\n",
                ),
            ),
            (
                "Unicode dash",
                lambda root: self.append_text(root / "README.md", "\n" + chr(0x2014) + "\n"),
            ),
        )

        for label, mutate in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp_dir:
                root = self.copy_repo(Path(temp_dir))
                mutate(root)
                result = self.run_check(root)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("ERROR:", result.stderr)

    def test_release_requires_manifest_tag_on_origin(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            root = self.copy_repo(temp_root)
            origin = temp_root / "origin.git"
            subprocess.run(
                ["git", "init", "--bare", str(origin)],
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                ["git", "-C", str(root), "init"],
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                ["git", "-C", str(root), "remote", "add", "origin", str(origin)],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(root), "config", "user.name", "Check Fixture"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(root), "config", "user.email", "check@example.com"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(root), "add", "-A"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(root), "commit", "-m", "Fixture"],
                check=True,
                capture_output=True,
                text=True,
            )

            missing = self.run_check(root, release=True)
            self.assertNotEqual(missing.returncode, 0, missing.stdout)
            self.assertIn("does not exist on origin", missing.stderr)

            tag = f"v{self.manifest_version(root)}"
            subprocess.run(
                ["git", "-C", str(root), "tag", tag],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(root), "push", "origin", f"refs/tags/{tag}"],
                check=True,
                capture_output=True,
                text=True,
            )
            present = self.run_check(root, release=True)
            self.assertEqual(present.returncode, 0, present.stderr)

    def set_codex_version(self, root: Path, version: str) -> None:
        path = root / ".codex-plugin" / "plugin.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["version"] = version
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def add_claude_skill_list(self, root: Path) -> None:
        path = root / ".claude-plugin" / "plugin.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["skills"] = ["implement"]
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def append_text(self, path: Path, value: str) -> None:
        path.write_text(path.read_text(encoding="utf-8") + value, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()

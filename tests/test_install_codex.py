from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "install-codex.sh"
SKILL_NAMES = sorted(path.parent.name for path in (REPO_ROOT / "skills").glob("*/SKILL.md"))


class InstallCodexTests(unittest.TestCase):
    def run_installer(
        self,
        destination: Path,
        *args: str,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            "bash",
            str(INSTALLER),
            "--source",
            str(REPO_ROOT),
            "--dest",
            str(destination),
            "--allow-plugin-duplicate",
            *args,
        ]
        return subprocess.run(
            command,
            check=False,
            text=True,
            capture_output=True,
            env=env,
        )

    def test_dry_run_makes_no_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            result = self.run_installer(destination, "--dry-run")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(destination.exists())
            self.assertIn("would install", result.stdout)

    def test_symlink_install_rerun_and_uninstall(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            first = self.run_installer(destination)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(
                sorted(path.name for path in destination.iterdir() if path.is_symlink()),
                SKILL_NAMES,
            )

            second = self.run_installer(destination)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("skipped:", second.stdout)
            self.assertTrue(all((destination / name).is_symlink() for name in SKILL_NAMES))

            removed = self.run_installer(destination, "--uninstall")
            self.assertEqual(removed.returncode, 0, removed.stderr)
            self.assertTrue(all(not (destination / name).exists() for name in SKILL_NAMES))

    def test_copy_install_is_idempotent_and_owned(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            first = self.run_installer(destination, "--copy")
            self.assertEqual(first.returncode, 0, first.stderr)
            marker = destination / "implement" / ".build-plugin-owner"
            self.assertIn("plugin=build", marker.read_text(encoding="utf-8"))

            second = self.run_installer(destination, "--copy")
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertTrue((destination / "implement" / "SKILL.md").is_file())

    def test_collision_preflight_prevents_partial_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            collision = destination / "idea-to-product-concept"
            collision.mkdir(parents=True)
            (collision / "keep.txt").write_text("mine\n", encoding="utf-8")

            result = self.run_installer(destination)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("No changes were made", result.stderr)
            self.assertEqual((collision / "keep.txt").read_text(encoding="utf-8"), "mine\n")
            self.assertFalse((destination / "evals-gate").exists())

    def test_stale_owned_copy_is_removed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            first = self.run_installer(destination)
            self.assertEqual(first.returncode, 0, first.stderr)

            stale = destination / "old-skill"
            stale.mkdir()
            marker = stale / ".build-plugin-owner"
            marker.write_text(
                f"plugin=build\nsource={REPO_ROOT}\nskill=old-skill\n",
                encoding="utf-8",
            )
            manifest = destination / ".build-managed"
            manifest.write_text(
                manifest.read_text(encoding="utf-8") + "skill=old-skill\n",
                encoding="utf-8",
            )

            result = self.run_installer(destination)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(stale.exists())
            self.assertIn("removed stale", result.stdout)

    def test_uninstall_preflight_preserves_everything_on_collision(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            first = self.run_installer(destination)
            self.assertEqual(first.returncode, 0, first.stderr)
            collision = destination / "implement"
            collision.unlink()
            collision.mkdir()
            (collision / "mine.txt").write_text("keep\n", encoding="utf-8")

            result = self.run_installer(destination, "--uninstall")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("No changes were made", result.stderr)
            self.assertTrue((destination / "evals-gate").is_symlink())
            self.assertEqual((collision / "mine.txt").read_text(encoding="utf-8"), "keep\n")
            self.assertTrue((destination / ".build-managed").is_file())

    def test_ref_must_match_source_head(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            good = self.run_installer(destination, "--dry-run", "--ref", "HEAD")
            self.assertEqual(good.returncode, 0, good.stderr)
            bad = self.run_installer(destination, "--dry-run", "--ref", "missing-ref")
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("Git ref does not exist", bad.stderr)

    def test_installed_universal_plugin_blocks_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            destination = temp_root / "skills"
            fake_bin = temp_root / "bin"
            fake_bin.mkdir()
            fake_codex = fake_bin / "codex"
            fake_codex.write_text(
                "#!/usr/bin/env bash\nprintf 'build@personal installed, enabled 2.1.0\\n'\n",
                encoding="utf-8",
            )
            fake_codex.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = f"{fake_bin}:{env['PATH']}"

            command = [
                "bash",
                str(INSTALLER),
                "--source",
                str(REPO_ROOT),
                "--dest",
                str(destination),
            ]
            result = subprocess.run(
                command,
                check=False,
                text=True,
                capture_output=True,
                env=env,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("universal plugin is already installed", result.stderr)
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()

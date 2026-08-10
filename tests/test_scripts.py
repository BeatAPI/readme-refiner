from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "beautify-readme" / "scripts"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ScriptTests(unittest.TestCase):
    def test_all_cover_presets_render_exact_title(self):
        renderer = load("render_cover")
        for style_id in renderer.load_presets():
            svg = renderer.render(style_id, "Exact Project", "Verified tagline")
            self.assertIn("Exact Project", svg)
            self.assertIn('role="img"', svg)
            self.assertNotIn("{{", svg)

    def test_inspector_reads_package_scripts(self):
        inspector = load("inspect_repository")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "package.json").write_text(
                json.dumps({"name": "demo", "scripts": {"test": "echo ok"}}), encoding="utf-8"
            )
            result = inspector.inventory(root)
            self.assertEqual(result["project_name"], "demo")
            self.assertEqual(result["manifests"]["package.json"]["scripts"], ["test"])

    def test_checker_reports_missing_local_path(self):
        checker = load("check_readme")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text(
                "![Project cover](assets/readme/cover.svg)\n\n# Demo\n", encoding="utf-8"
            )
            result = checker.check(readme)
            self.assertFalse(result["ok"])
            self.assertEqual(result["summary"]["errors"], 1)

    def test_repository_readme_passes_path_checks(self):
        checker = load("check_readme")
        result = checker.check(ROOT / "README.md")
        self.assertTrue(result["ok"], result["findings"])
        self.assertEqual(result["summary"]["warnings"], 0, result["findings"])

    def test_checker_recognizes_html_cover(self):
        checker = load("check_readme")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "assets").mkdir()
            (root / "assets" / "cover.svg").write_text("<svg/>", encoding="utf-8")
            readme = root / "README.md"
            readme.write_text(
                '<p><img src="assets/cover.svg" alt="Project cover" /></p>\n\n# Demo\n',
                encoding="utf-8",
            )
            result = checker.check(readme)
            self.assertTrue(result["ok"])
            self.assertEqual(result["summary"]["warnings"], 0)
            self.assertEqual(result["summary"]["local_images"], 1)


if __name__ == "__main__":
    unittest.main()

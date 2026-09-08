from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "refine-readme" / "scripts"


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
            self.assertNotIn("README REFINER", svg)
            self.assertNotIn("BEAUTIFUL · TRUE", svg)

    def test_cover_uses_only_explicit_project_labels(self):
        renderer = load("render_cover")
        svg = renderer.render(
            "protocol-grid",
            "BeatAPI for Dify",
            "Create and monitor async video tasks",
            eyebrow="DIFY PLUGIN",
            badge="2 VERIFIED TOOLS",
            proof_label="CREATE → POLL",
        )
        self.assertIn("DIFY PLUGIN", svg)
        self.assertIn("2 VERIFIED TOOLS", svg)
        self.assertIn("CREATE → POLL", svg)

    def test_cover_rejects_markup_in_color_override(self):
        renderer = load("render_cover")
        with self.assertRaises(ValueError):
            renderer.render(
                "protocol-grid",
                "Demo",
                "Verified tagline",
                accent_override='red" onload="alert(1)',
            )

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
            self.assertEqual(result["readme_excerpt"], "# Demo")

    def test_inspector_reads_pyproject_and_private_asset_folder(self):
        inspector = load("inspect_repository")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Python Demo\n", encoding="utf-8")
            (root / "pyproject.toml").write_text(
                '[project]\nname = "python-demo"\ndescription = "A useful CLI"\n'
                'requires-python = ">=3.11"\n\n[project.scripts]\ndemo = "demo:main"\n',
                encoding="utf-8",
            )
            (root / "_assets").mkdir()
            (root / "_assets" / "preview.webp").write_bytes(b"RIFF")
            result = inspector.inventory(root)
            self.assertEqual(result["project_name"], "python-demo")
            self.assertEqual(result["manifests"]["pyproject.toml"]["scripts"], ["demo"])
            self.assertEqual(result["existing_visual_assets"], ["_assets/preview.webp"])

    def test_direction_planner_returns_three_evidence_led_candidates(self):
        planner = load("plan_directions")
        result = planner.recommend({
            "root": "/tmp/beatapi-dify-plugin",
            "project_name": "beatapi-dify-plugin",
            "headings": [{"text": "Dify plugin for an asynchronous API"}],
            "manifests": {},
            "existing_visual_assets": ["assets/demo-output.webp"],
        })
        self.assertEqual(result["direction_gate"]["status"], "ready")
        self.assertEqual(len(result["directions"]), 3)
        self.assertEqual(result["directions"][0]["style_seed"], "integration-bridge")
        self.assertEqual(result["directions"][0]["construction_mode"], "proof-composite")

    def test_direction_planner_blocks_when_repository_has_no_style_evidence(self):
        planner = load("plan_directions")
        result = planner.recommend({
            "root": "/tmp/unknown",
            "project_name": "unknown",
            "headings": [],
            "manifests": {},
            "existing_visual_assets": [],
        })
        self.assertEqual(result["direction_gate"]["status"], "blocked")
        self.assertEqual(result["directions"], [])

    def test_direction_planner_does_not_pad_with_zero_evidence_styles(self):
        planner = load("plan_directions")
        result = planner.recommend({
            "root": "/tmp/api-only",
            "project_name": "api-only",
            "headings": [],
            "manifests": {},
            "existing_visual_assets": [],
        })
        self.assertEqual(result["direction_gate"]["status"], "blocked")
        self.assertEqual(len(result["directions"]), 1)
        self.assertTrue(all(item["evidence_score"] > 0 for item in result["directions"]))

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

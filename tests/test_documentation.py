import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_has_beginner_commands_for_every_model() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "cd ~/桌面/onerobot_h1-pybullet" in readme
    assert "bash scripts/open_demo.sh right" in readme
    assert "bash scripts/open_demo.sh left" in readme
    assert "bash scripts/open_demo.sh bimanual" in readme
    assert "bash scripts/validate_all.sh" in readme
    assert "ecf530911284ba0e559f7a24dc222fd8e60d31ed" in readme
    assert "CC BY 4.0" in readme


def test_publication_record_explains_personal_and_official_destinations() -> None:
    publishing = (ROOT / "docs" / "PUBLISHING.md").read_text(encoding="utf-8")
    assert "uniquemelody/onerobot_h1-pybullet" in publishing
    assert "bulletphysics/bullet3" in publishing
    assert "examples/pybullet/gym/pybullet_data" in publishing
    assert "Pull Request" in publishing


def test_validation_script_exists_is_executable_and_has_valid_shell_syntax() -> None:
    script = ROOT / "scripts" / "validate_all.sh"
    assert script.is_file()
    assert os.access(script, os.X_OK)
    result = subprocess.run(
        ["bash", "-n", str(script)], check=False, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr

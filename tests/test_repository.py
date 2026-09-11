from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SOURCE_COMMIT = "ecf530911284ba0e559f7a24dc222fd8e60d31ed"


def test_model_registry_locks_source_and_three_models() -> None:
    registry_path = ROOT / "config" / "models.yaml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))

    assert registry["source_repository"] == "https://github.com/katazen/onerobot_h1"
    assert registry["source_commit"] == EXPECTED_SOURCE_COMMIT
    assert set(registry["models"]) == {"right", "left", "bimanual"}
    assert registry["models"]["right"]["movable_joint_count"] == 7
    assert registry["models"]["left"]["movable_joint_count"] == 7
    assert registry["models"]["bimanual"]["movable_joint_count"] == 14


def test_required_license_records_exist() -> None:
    for relative_path in (
        "LICENSE",
        "LICENSES/CC-BY-4.0.txt",
        "ASSET_LICENSE_STATUS.md",
        "THIRD_PARTY_NOTICES.md",
    ):
        assert (ROOT / relative_path).is_file(), relative_path


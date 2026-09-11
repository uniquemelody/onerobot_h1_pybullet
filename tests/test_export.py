from __future__ import annotations

import hashlib
import json
import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path

import pytest

from onerobotics_a1_pybullet.export import export_all

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "source" / "A1_2026"


def _tree_bytes(path: Path, *, drop_mujoco: bool = False) -> bytes:
    root = deepcopy(ET.parse(path).getroot())
    if drop_mujoco:
        for mujoco in root.findall("mujoco"):
            root.remove(mujoco)
    for element in root.iter():
        if element.text is not None and not element.text.strip():
            element.text = None
        if element.tail is not None and not element.tail.strip():
            element.tail = None
    return ET.tostring(root, encoding="utf-8")


def _directory_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_export_is_deterministic_and_records_provenance(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"

    export_all(first)
    export_all(second)

    assert _directory_hashes(first) == _directory_hashes(second)
    manifest = json.loads((first / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["source_commit"] == "ecf530911284ba0e559f7a24dc222fd8e60d31ed"
    assert set(manifest["models"]) == {"right", "left", "bimanual"}


@pytest.mark.parametrize(
    ("model_name", "source_relative", "mesh_count"),
    [
        ("onerobotics_a1_right_arm", "a1_r.urdf", 8),
        ("onerobotics_a1_left_arm", "a1_l.urdf", 8),
        (
            "onerobotics_a1_bimanual_stand",
            "bimanual_stand/a1_bimanual_stand.urdf",
            17,
        ),
    ],
)
def test_exported_urdf_is_portable_and_physically_unchanged(
    tmp_path: Path, model_name: str, source_relative: str, mesh_count: int
) -> None:
    export_all(tmp_path)
    model_directory = tmp_path / model_name
    urdf_path = model_directory / "model.urdf"

    assert _tree_bytes(urdf_path) == _tree_bytes(
        SOURCE_ROOT / source_relative, drop_mujoco=True
    )
    root = ET.parse(urdf_path).getroot()
    assert root.find("mujoco") is None
    assert (model_directory / "LICENSE.txt").is_file()
    assert "Creative Commons Attribution 4.0" in (
        model_directory / "LICENSE.txt"
    ).read_text(encoding="utf-8")
    assert "OneRobotics A1 robot assets" in (
        model_directory / "README.md"
    ).read_text(encoding="utf-8")

    meshes = [element.attrib["filename"] for element in root.findall(".//mesh")]
    assert len(set(meshes)) == mesh_count
    for mesh in meshes:
        relative = Path(mesh)
        assert not relative.is_absolute()
        assert ".." not in relative.parts
        assert (model_directory / relative).is_file()

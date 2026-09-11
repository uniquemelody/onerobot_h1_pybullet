from __future__ import annotations

import hashlib
import json
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

from onerobotics_a1_pybullet.models import PROJECT_ROOT, models


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _parse_with_comments(path: Path) -> ET.ElementTree:
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    return ET.parse(path, parser=parser)


def _safe_mesh_source(source_urdf: Path, mesh_uri: str) -> Path:
    relative = Path(mesh_uri)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Mesh URI must be repository-relative: {mesh_uri}")
    source = (source_urdf.parent / relative).resolve()
    source_root = (PROJECT_ROOT / "source" / "A1_2026").resolve()
    if not source.is_relative_to(source_root):
        raise ValueError(f"Mesh escapes source root: {mesh_uri}")
    if not source.is_file():
        raise FileNotFoundError(source)
    return source


def _export_model(key: str, output_root: Path) -> dict[str, object]:
    spec = models()[key]
    model_directory = output_root / spec.asset_directory
    if model_directory.exists():
        shutil.rmtree(model_directory)
    model_directory.mkdir(parents=True)

    tree = _parse_with_comments(spec.source_urdf)
    root = tree.getroot()
    for mujoco in root.findall("mujoco"):
        root.remove(mujoco)

    mesh_uris = sorted({mesh.attrib["filename"] for mesh in root.findall(".//mesh")})
    for mesh_uri in mesh_uris:
        source = _safe_mesh_source(spec.source_urdf, mesh_uri)
        destination = model_directory / Path(mesh_uri)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    ET.indent(tree, space="  ")
    urdf_path = model_directory / "model.urdf"
    tree.write(urdf_path, encoding="utf-8", xml_declaration=True)

    metadata = {
        "asset_license": "CC-BY-4.0",
        "changes": [
            "Removed the unused top-level MuJoCo compiler element for PyBullet portability.",
            "Packaged referenced meshes in a self-contained model directory.",
            "Physical model fields are unchanged.",
        ],
        "display_name": spec.display_name,
        "model_key": key,
        "source_commit": "ecf530911284ba0e559f7a24dc222fd8e60d31ed",
        "source_repository": "https://github.com/katazen/onerobot_h1",
        "source_urdf": spec.source_urdf.relative_to(PROJECT_ROOT).as_posix(),
    }
    (model_directory / "metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    shutil.copy2(PROJECT_ROOT / "LICENSES" / "CC-BY-4.0.txt", model_directory / "LICENSE.txt")
    (model_directory / "README.md").write_text(
        f"# {spec.display_name}\n\n"
        "OneRobotics A1 robot assets © 2026 OneRobotics, licensed under "
        "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).\n\n"
        "Source: <https://github.com/katazen/onerobot_h1> at commit "
        "`ecf530911284ba0e559f7a24dc222fd8e60d31ed`.\n\n"
        "Changes: removed the unused top-level MuJoCo compiler element and packaged "
        "the referenced meshes beside `model.urdf`; physical model fields are unchanged.\n",
        encoding="utf-8",
    )

    files = {
        path.relative_to(model_directory).as_posix(): _sha256(path)
        for path in sorted(model_directory.rglob("*"))
        if path.is_file()
    }
    return {
        "asset_directory": spec.asset_directory,
        "files": files,
        "movable_joint_count": spec.movable_joint_count,
    }


def export_all(output_root: Path | None = None) -> Path:
    destination = output_root or PROJECT_ROOT / "assets"
    destination.mkdir(parents=True, exist_ok=True)
    registry = yaml.safe_load((PROJECT_ROOT / "config" / "models.yaml").read_text())
    exported = {key: _export_model(key, destination) for key in models()}
    manifest = {
        "schema_version": 1,
        "source_commit": registry["source_commit"],
        "source_repository": registry["source_repository"],
        "models": exported,
    }
    (destination / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return destination

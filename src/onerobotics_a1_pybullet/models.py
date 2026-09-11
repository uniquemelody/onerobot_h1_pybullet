from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = PROJECT_ROOT / "config" / "models.yaml"


@dataclass(frozen=True)
class ModelSpec:
    key: str
    display_name: str
    source_urdf: Path
    asset_directory: str
    movable_joint_count: int
    movable_joint_names: tuple[str, ...]

    @property
    def urdf_path(self) -> Path:
        return PROJECT_ROOT / "assets" / self.asset_directory / "model.urdf"


@lru_cache(maxsize=1)
def models() -> dict[str, ModelSpec]:
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    source_root = PROJECT_ROOT / registry["source_root"]
    return {
        key: ModelSpec(
            key=key,
            display_name=value["display_name"],
            source_urdf=source_root / value["source_urdf"],
            asset_directory=value["asset_directory"],
            movable_joint_count=value["movable_joint_count"],
            movable_joint_names=tuple(value["movable_joint_names"]),
        )
        for key, value in registry["models"].items()
    }


def get_model(key: str) -> ModelSpec:
    try:
        return models()[key]
    except KeyError as error:
        valid = ", ".join(models())
        raise ValueError(f"Unknown model {key!r}; choose one of: {valid}") from error


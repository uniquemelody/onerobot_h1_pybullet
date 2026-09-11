from __future__ import annotations

import argparse
import json
import time
from collections.abc import Sequence

import pybullet as p
import pybullet_data

from onerobotics_a1_pybullet.loader import (
    command_safe_pose,
    connect,
    disconnect,
    joint_infos,
    load_model,
)
from onerobotics_a1_pybullet.models import get_model, models

CAMERAS = {
    "right": (0.85, 40.0, -25.0, (0.0, 0.0, 0.18)),
    "left": (0.85, 140.0, -25.0, (0.0, 0.0, 0.18)),
    "bimanual": (1.25, 45.0, -22.0, (0.0, 0.0, 0.30)),
}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="View a OneRobotics A1 model in PyBullet")
    parser.add_argument("model", choices=tuple(models()), nargs="?", default="right")
    parser.add_argument("--direct", action="store_true", help="validate without opening a window")
    parser.add_argument(
        "--steps", type=int, default=480, help="simulation steps used to reach the demo pose"
    )
    return parser


def run_demo(model_key: str, *, gui: bool, steps: int) -> dict[str, object]:
    if steps < 0:
        raise ValueError("steps must be zero or greater")
    client_id = connect(gui=gui)
    try:
        p.setAdditionalSearchPath(pybullet_data.getDataPath(), physicsClientId=client_id)
        p.loadURDF("plane.urdf", basePosition=(0.0, 0.0, -0.03), physicsClientId=client_id)
        body_id = load_model(model_key, client_id=client_id)

        if gui:
            distance, yaw, pitch, target = CAMERAS[model_key]
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0, physicsClientId=client_id)
            p.resetDebugVisualizerCamera(
                cameraDistance=distance,
                cameraYaw=yaw,
                cameraPitch=pitch,
                cameraTargetPosition=target,
                physicsClientId=client_id,
            )

        command_safe_pose(body_id, client_id=client_id, steps=steps)
        movable = [joint for joint in joint_infos(body_id, client_id) if joint.movable]
        summary = {
            "connection_mode": "GUI" if gui else "DIRECT",
            "display_name": get_model(model_key).display_name,
            "model": model_key,
            "movable_joint_count": len(movable),
            "movable_joint_names": [joint.name for joint in movable],
            "status": "loaded",
        }

        if gui:
            print("模型已正确加载。关闭 PyBullet 窗口或按 Ctrl+C 退出。")
            while p.isConnected(client_id):
                p.stepSimulation(physicsClientId=client_id)
                time.sleep(1.0 / 200.0)
        return summary
    finally:
        disconnect(client_id)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    summary = run_demo(arguments.model, gui=not arguments.direct, steps=arguments.steps)
    if arguments.direct:
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


from __future__ import annotations

from dataclasses import dataclass

import pybullet as p

from onerobotics_a1_pybullet.models import get_model


@dataclass(frozen=True)
class JointInfo:
    index: int
    name: str
    joint_type: int
    lower: float
    upper: float
    maximum_force: float
    maximum_velocity: float

    @property
    def movable(self) -> bool:
        return self.joint_type != p.JOINT_FIXED


def connect(*, gui: bool) -> int:
    client_id = p.connect(p.GUI if gui else p.DIRECT)
    if client_id < 0:
        mode = "GUI" if gui else "DIRECT"
        raise RuntimeError(f"Could not connect to PyBullet in {mode} mode")
    p.resetSimulation(physicsClientId=client_id)
    p.setPhysicsEngineParameter(fixedTimeStep=1.0 / 200.0, physicsClientId=client_id)
    p.setGravity(0.0, 0.0, -9.81, physicsClientId=client_id)
    return client_id


def disconnect(client_id: int) -> None:
    if p.isConnected(client_id):
        p.disconnect(physicsClientId=client_id)


def load_model(model_key: str, *, client_id: int, fixed_base: bool = True) -> int:
    spec = get_model(model_key)
    if not spec.urdf_path.is_file():
        raise FileNotFoundError(
            f"Generated asset is missing: {spec.urdf_path}. Run scripts/export_assets.py first."
        )
    return p.loadURDF(
        str(spec.urdf_path),
        useFixedBase=fixed_base,
        flags=p.URDF_USE_INERTIA_FROM_FILE,
        physicsClientId=client_id,
    )


def joint_infos(body_id: int, client_id: int) -> tuple[JointInfo, ...]:
    result = []
    for index in range(p.getNumJoints(body_id, physicsClientId=client_id)):
        raw = p.getJointInfo(body_id, index, physicsClientId=client_id)
        result.append(
            JointInfo(
                index=raw[0],
                name=raw[1].decode("utf-8"),
                joint_type=raw[2],
                lower=raw[8],
                upper=raw[9],
                maximum_force=raw[10],
                maximum_velocity=raw[11],
            )
        )
    return tuple(result)


def _safe_target(joint: JointInfo) -> float:
    margin = min(0.05, (joint.upper - joint.lower) * 0.1)
    return min(max(0.15, joint.lower + margin), joint.upper - margin)


def command_safe_pose(body_id: int, *, client_id: int, steps: int = 480) -> tuple[float, ...]:
    movable = [joint for joint in joint_infos(body_id, client_id) if joint.movable]
    targets = tuple(_safe_target(joint) for joint in movable)
    for order, (joint, target) in enumerate(zip(movable, targets, strict=True)):
        force = 26.859 if order % 7 < 3 else 5.975
        p.setJointMotorControl2(
            bodyUniqueId=body_id,
            jointIndex=joint.index,
            controlMode=p.POSITION_CONTROL,
            targetPosition=target,
            force=force,
            positionGain=0.3,
            velocityGain=1.0,
            physicsClientId=client_id,
        )
    for _ in range(steps):
        p.stepSimulation(physicsClientId=client_id)
    return targets


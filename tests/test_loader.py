import math

import pybullet as p
import pytest

from onerobotics_a1_pybullet.loader import (
    command_safe_pose,
    connect,
    disconnect,
    joint_infos,
    load_model,
)
from onerobotics_a1_pybullet.models import get_model


def test_unknown_model_has_beginner_friendly_error() -> None:
    with pytest.raises(ValueError, match="choose one of: right, left, bimanual"):
        get_model("wrong")


@pytest.mark.parametrize("model_key", ["right", "left", "bimanual"])
def test_model_loads_with_expected_movable_joints(model_key: str) -> None:
    client_id = connect(gui=False)
    try:
        body_id = load_model(model_key, client_id=client_id)
        movable = [joint for joint in joint_infos(body_id, client_id) if joint.movable]
        spec = get_model(model_key)

        assert len(movable) == spec.movable_joint_count
        assert tuple(joint.name for joint in movable) == spec.movable_joint_names
        assert all(math.isfinite(joint.lower) for joint in movable)
        assert all(math.isfinite(joint.upper) for joint in movable)
        assert all(joint.lower < joint.upper for joint in movable)
    finally:
        disconnect(client_id)


@pytest.mark.parametrize("model_key", ["right", "left", "bimanual"])
def test_safe_position_command_moves_joints(model_key: str) -> None:
    client_id = connect(gui=False)
    try:
        body_id = load_model(model_key, client_id=client_id)
        movable = [joint for joint in joint_infos(body_id, client_id) if joint.movable]
        before = [
            p.getJointState(body_id, joint.index, physicsClientId=client_id)[0]
            for joint in movable
        ]

        targets = command_safe_pose(body_id, client_id=client_id, steps=480)
        after = [
            p.getJointState(body_id, joint.index, physicsClientId=client_id)[0]
            for joint in movable
        ]

        assert len(targets) == len(movable)
        assert all(math.isfinite(position) for position in after)
        assert all(
            joint.lower <= position <= joint.upper
            for joint, position in zip(movable, after, strict=True)
        )
        assert max(abs(end - start) for start, end in zip(before, after, strict=True)) > 0.05
        assert max(abs(end - target) for end, target in zip(after, targets, strict=True)) < 0.05
    finally:
        disconnect(client_id)

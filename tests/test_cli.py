import json
import os
import subprocess
from pathlib import Path

import pytest

from onerobotics_a1_pybullet import demo

ROOT = Path(__file__).resolve().parents[1]
OPEN_DEMO = ROOT / "scripts" / "open_demo.sh"


def _clean_environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    return environment


@pytest.mark.parametrize(
    ("model_key", "joint_count"),
    [("right", 7), ("left", 7), ("bimanual", 14)],
)
def test_beginner_launcher_runs_from_any_directory(
    tmp_path: Path, model_key: str, joint_count: int
) -> None:
    result = subprocess.run(
        [str(OPEN_DEMO), model_key, "--direct", "--steps", "5"],
        cwd=tmp_path,
        env=_clean_environment(),
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["model"] == model_key
    assert summary["movable_joint_count"] == joint_count
    assert summary["connection_mode"] == "DIRECT"


def test_beginner_launcher_rejects_unknown_model(tmp_path: Path) -> None:
    result = subprocess.run(
        [str(OPEN_DEMO), "wrong", "--direct"],
        cwd=tmp_path,
        env=_clean_environment(),
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 2
    assert "invalid choice" in result.stderr


def test_shell_scripts_are_executable() -> None:
    for path in (ROOT / "scripts" / "setup.sh", OPEN_DEMO):
        assert path.is_file()
        assert os.access(path, os.X_OK), path


def test_ctrl_c_exits_without_traceback(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def interrupt(*args: object, **kwargs: object) -> dict[str, object]:
        raise KeyboardInterrupt

    monkeypatch.setattr(demo, "run_demo", interrupt)

    assert demo.main(["right"]) == 0
    assert "已退出" in capsys.readouterr().out

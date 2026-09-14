# OneRobotics A1 PyBullet Assets — Design

## Goal

Publish a beginner-friendly, independently testable PyBullet adaptation of the
three public OneRobotics A1 assets already validated for Gazebo: right arm,
left arm, and bimanual stand.

## Decision

Use a standalone `onerobot_h1-pybullet` repository. This keeps simulator
integration separate from the upstream robot source and from the Gazebo
deliverable. The tested asset folders can later be proposed to
`bulletphysics/bullet3` in a pull request if upstream inclusion is desired.

Alternatives considered:

1. Add PyBullet files to `onerobot_h1-gazebo`: fewer repositories, but mixes
   unrelated simulator deliverables and gives the repository a misleading name.
2. Fork `bulletphysics/bullet3` immediately: closest to an upstream PR, but
   unnecessarily large before the upstream scope and acceptance requirements
   are confirmed.

## Source and licensing

- Source repository: `https://github.com/katazen/onerobot_h1`
- Source commit: `ecf530911284ba0e559f7a24dc222fd8e60d31ed`
- Asset source root: `source/h1_reach/h1_reach/assets/urdf/A1_2026`
- Asset license: CC BY 4.0, preserved with attribution and third-party notices.

The three source URDF trees are copied into self-contained model directories.
Only PyBullet compatibility changes are allowed: portable relative mesh paths,
removal of simulator-specific top-level tags that PyBullet does not use, and
documented defaults for loading. Geometry, joint transforms, joint limits,
inertial values, and visual colors must remain source-equivalent.

## Repository layout

```text
assets/
  onerobotics_a1_right_arm/model.urdf
  onerobotics_a1_left_arm/model.urdf
  onerobotics_a1_bimanual_stand/model.urdf
src/onerobotics_a1_pybullet/
  models.py        # authoritative model registry
  loader.py        # safe PyBullet loading and inspection
  demo.py          # GUI / DIRECT demo entry point
scripts/
  setup.sh         # beginner setup
  open_demo.sh     # beginner launcher
tests/             # static and PyBullet DIRECT tests
docs/
  PUBLISHING.md    # publication status and upstream contribution guide
```

## Runtime behavior

`open_demo.sh` accepts `right`, `left`, or `bimanual`. The Python demo connects
to the PyBullet GUI, loads a plane and the selected fixed-base robot, positions
the camera, and moves joints through conservative in-limit targets. A `--direct`
mode runs without a window for automated validation.

The loader resolves assets from the installed/source repository rather than the
current shell directory. It rejects unknown model names, verifies successful
connection and loading, exposes joint metadata, and always disconnects cleanly.

## Verification

Automated tests must prove that:

- all URDF and mesh paths exist and remain inside the repository;
- all three models load in PyBullet `DIRECT` mode without missing assets;
- right and left expose 7 movable joints and bimanual exposes 14;
- joint names and limits match the source specification;
- conservative joint commands produce finite, changed states;
- source commit, license, and generated asset hashes are recorded;
- the documented copy-paste commands work from outside the repository.

Manual acceptance is one GUI launch per model and a saved screenshot or written
record. External publication occurs only after local verification passes.

# OneRobotics A1 PyBullet Assets — Implementation Plan

**Goal:** Build, verify, document, and prepare three self-contained A1 PyBullet
assets for publication.

**Architecture:** A small Python package owns the model registry, loader, asset
validator, and demo. Source-locked URDF/mesh folders are checked into `assets/`.
PyBullet 3.2.7 runs under a uv-managed Python 3.11 environment. Tests use
PyBullet DIRECT so they work without a display.

**Tech stack:** Python 3.11, PyBullet 3.2.7, uv, pytest, ruff.

---

### Task 1: Repository and provenance foundation

**Files:** `pyproject.toml`, `README.md`, `.gitignore`, `LICENSES/*`,
`THIRD_PARTY_NOTICES.md`, `config/models.yaml`.

1. Add tests that require the exact three model definitions and source commit.
2. Run the tests and confirm they fail because the files do not exist.
3. Add the minimal project metadata, model registry, and license records.
4. Run focused tests and commit.

### Task 2: Reproducible asset export

**Files:** `src/onerobotics_a1_pybullet/export.py`, `scripts/export_assets.py`,
`assets/**`, `tests/test_export.py`, `tests/test_assets.py`.

1. Add failing tests for portable paths, source preservation, deterministic
   output, and expected asset inventory.
2. Implement the smallest deterministic exporter.
3. Copy the source-locked input files, generate all three model folders, and
   write SHA-256 manifests.
4. Run focused tests and commit.

### Task 3: PyBullet loader and physical smoke tests

**Files:** `src/onerobotics_a1_pybullet/models.py`, `loader.py`,
`tests/test_loader.py`, `tests/test_runtime.py`.

1. Add failing tests for model lookup, load results, movable joint counts,
   expected names/limits, and conservative movement.
2. Implement loading with explicit client IDs and fixed-base defaults.
3. Run tests in DIRECT mode and correct only demonstrated compatibility issues.
4. Commit after all focused tests pass.

### Task 4: Beginner demo and launch scripts

**Files:** `src/onerobotics_a1_pybullet/demo.py`, `scripts/setup.sh`,
`scripts/open_demo.sh`, `tests/test_cli.py`.

1. Add failing CLI tests for all three names, `--direct`, and execution from a
   different working directory.
2. Implement GUI/DIRECT entry points, camera presets, safe poses, and cleanup.
3. Run CLI tests and one headless demo per model.
4. Commit.

### Task 5: Documentation, package validation, and publication preparation

**Files:** `README.md`, `docs/PUBLISHING.md`, `VALIDATION.md`,
`scripts/validate_all.sh`, `tests/test_documentation.py`.

1. Add failing checks for copy-paste commands, attribution, and clean archive
   inventory.
2. Write the zero-background quick start and mentor-facing publication record.
3. Run `pytest`, `ruff check`, the full validation script, and GUI validation.
4. Review the git diff and commit the verified deliverable.
5. Create/push the user's GitHub repository if an authenticated creation method
   is available; otherwise provide the single required browser step and push
   immediately after the empty repository exists.


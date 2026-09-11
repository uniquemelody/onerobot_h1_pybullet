# Validation record

- Date: 2026-09-11
- Platform: Ubuntu Linux, x86_64
- Python: 3.11
- PyBullet: 3.2.7
- Source commit: `ecf530911284ba0e559f7a24dc222fd8e60d31ed`

The authoritative command is:

```bash
bash scripts/validate_all.sh
```

It verifies source hashes, deterministically regenerates the three asset
folders, checks that generation produces no Git diff, runs the complete pytest
and ruff suites, and loads/moves all three models in PyBullet DIRECT mode.

Expected movable joints:

| Model | Movable joints |
|---|---:|
| Right arm | 7 |
| Left arm | 7 |
| Bimanual stand | 14 |

Final local result on 2026-09-11:

- 22 pytest checks passed;
- ruff reported `All checks passed!`;
- right, left, and bimanual returned `status: loaded` in DIRECT mode;
- the right-arm GUI opened with an NVIDIA OpenGL 3.3 context and displayed the
  success message;
- `Ctrl+C` cleanly exits without a traceback.

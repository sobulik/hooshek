import pathlib
import subprocess


def run(
    command: list[str], project_path: pathlib.Path, tmp_path: pathlib.Path
) -> subprocess.CompletedProcess:
    cmd = (
        ["uv", "run", "--no-sync", "--project", project_path]
        + [project_path / "src" / "hooshek" / command[0]]
        + command[1:]
    )
    return subprocess.run(cmd, cwd=tmp_path, check=True)

# ruff: noqa: S603

from pathlib import Path
from subprocess import PIPE, Popen

RESOURCE_PATH = "tests/resources"

def run_test(script: Path, test_file: Path) -> tuple[str, str, int]:
    command = ["uv", "run", str(script), str(test_file)]
    process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)
    out, err = process.communicate()
    code = process.returncode
    return (out, err, code)

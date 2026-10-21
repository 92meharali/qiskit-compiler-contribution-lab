"""Check notebook-defined solutions using shared lab contracts."""

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

import cloudpickle

from qclab.labs import LABS


@dataclass(frozen=True)
class CheckResult:
    """Captured pytest output; a failed exercise is a result, not a kernel error."""

    returncode: int
    output: str

    @property
    def passed(self):
        return self.returncode == 0


def check_solution(solution, *, lab="01"):
    """Check the current callable in a fresh process with the shared acceptance suite.

    The snapshot includes referenced globals and closures. Temporary files are
    removed afterwards; no learner file is overwritten. Execution is limited to
    30 seconds, just as with the CLI checker.
    """
    if lab not in LABS:
        raise ValueError("Unknown lab. Choose '01' or '02'.")
    export, filename = LABS[lab]
    if not callable(solution):
        raise TypeError(f"Pass the function itself or pass class: check_solution({export})")
    with TemporaryDirectory(prefix="qclab-notebook-") as directory:
        directory = Path(directory)
        snapshot = directory / "solution.pkl"
        with snapshot.open("wb") as stream:
            cloudpickle.dump(solution, stream)
        module = directory / "solution.py"
        module.write_text(
            "import cloudpickle\n"
            f"with open({str(snapshot)!r}, 'rb') as stream:\n"
            f"    {export} = cloudpickle.load(stream)\n",
            encoding="utf-8",
        )
        suite = Path(__file__).parent / "checks" / filename
        env = os.environ.copy()
        env.pop("PYTEST_ADDOPTS", None)
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    str(suite),
                    "--solution",
                    str(module),
                    "-q",
                    "--tb=short",
                ],
                cwd=directory,
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            return CheckResult(2, "Checker timed out after 30 seconds. Look for an infinite loop.")
        return CheckResult(result.returncode, result.stdout + result.stderr)

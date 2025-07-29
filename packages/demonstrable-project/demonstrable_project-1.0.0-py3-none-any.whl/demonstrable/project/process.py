import logging
import subprocess
import sys

import exit_codes
from demonstrable.exception import ConfigurationError

logger = logging.getLogger(__name__)


class SubprocessError(ConfigurationError):
    """An error caused by a subprocess failure.

    No stack trace will be shown for this error.
    """


def run_process(command, cwd):
    try:
        subprocess.run(command, cwd=cwd, shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        stdout = e.output.decode('utf-8')
        stderr = e.stderr.decode('utf-8')
        lines = [
            f"Command '{command}' failed with exit code {e.returncode}."
        ]
        if stdout:
            lines.append(f"Output: {stdout}")
        if stderr:
            lines.append(f"Error: {stderr}")
        raise SubprocessError(
            "\n".join(lines)
        ) from e

import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def run_command(message: str, command: str, *, cwd: Optional[str] = None) -> None:
    """Execute a shell command, log its output and errors.

    Parameters
    ----------
    message: str
        Message displayed before running the command.
    command: str
        The shell command to execute.
    cwd: Optional[str]
        Working directory for the command.
    """
    logger.info(message)
    try:
        completed = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.stdout:
            logger.info(completed.stdout.strip())
        if completed.stderr:
            logger.error(completed.stderr.strip())
    except Exception as exc:
        logger.exception("Error running command %r: %s", command, exc)

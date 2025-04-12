from pathlib import Path
import platform


def make_venv_bin(venv: Path) -> Path:
    """Create a venv binary path for the current platform."""
    bin = 'Scripts' if platform.system() == 'Windows' else 'bin'
    return venv / bin

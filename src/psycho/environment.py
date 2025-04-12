import os
import shutil
from typing import Dict, Optional


def location(name: str) -> Optional[str]:
    """Return the path to the executable of the given name."""
    return shutil.which(name)


def environment() -> Dict[str, str]:
    """Return the path to the current Python environment."""
    return {
        name: value
        for name, value in os.environ.items()
    }

import json
from pathlib import Path

from ._version import __version__
# Import the necessary functions from the new modules
from .extension import _jupyter_server_extension_points, _load_jupyter_server_extension

HERE = Path(__file__).parent.resolve()

with (HERE / "labextension" / "package.json").open() as fid:
    data = json.load(fid)

def _jupyter_labextension_paths():
    """Defines the LabExtension path."""
    return [{
        "src": "labextension",
        "dest": data["name"]
    }]

# Expose the functions for Jupyter
# The actual implementation is now in extension.py
jupyter_server_extension_points = _jupyter_server_extension_points
load_jupyter_server_extension = _load_jupyter_server_extension

import os
from importlib.resources import files

import ddx_python
from ddx_python._ddx_python import *

from .config import *

__doc__ = ddx_python._ddx_python.__doc__
if hasattr(ddx_python._ddx_python, "__all__"):
    __all__ = ddx_python._ddx_python.__all__ + ["load_mainnet", "load_testnet"]

if os.environ.get("APP_CONFIG") is None:
    # FIXME: might need to change this environment variable to `DDX_APP_CONFIG` for better convention
    os.environ["APP_CONFIG"] = str(files("ddx_python") / "app_config")
    load_mainnet()

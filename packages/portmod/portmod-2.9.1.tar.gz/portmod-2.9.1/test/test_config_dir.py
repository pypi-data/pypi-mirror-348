import os
import sys

import pytest

from portmod.globals import env


@pytest.mark.skipif(
    "CI" not in os.environ,
    reason="Paths may differ from system to system; this just tests the default paths",
)
def test_config_dir():
    """Test that the CONFIG_DIR matches what is in the documentation. This may"""
    if sys.platform == "linux":
        assert env.CONFIG_DIR == os.path.expanduser("~/.config/portmod")
    elif sys.platform == "win32":
        assert env.CONFIG_DIR == os.path.expanduser(
            r"~\AppData\Roaming\portmod\portmod\config"
        )
    elif sys.platform == "darwin":
        assert env.CONFIG_DIR == os.path.expanduser(
            "~/Library/Preferences/portmod.portmod"
        )

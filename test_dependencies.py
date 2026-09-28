import os
import subprocess

import pytest

ROOT = os.path.dirname(os.path.abspath(__file__))

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("requirements", ["requirements.txt",
                                          "requirements-dev.txt"])
def test_dependencies_have_no_known_vulnerabilities(requirements):
    """Asks the Python Packaging Advisory Database (needs network)."""
    audit = subprocess.run(
        ["pip-audit", "--requirement", requirements,
         "--progress-spinner", "off"],
        cwd=ROOT, capture_output=True, text=True
    )

    assert audit.returncode == 0, audit.stdout + audit.stderr

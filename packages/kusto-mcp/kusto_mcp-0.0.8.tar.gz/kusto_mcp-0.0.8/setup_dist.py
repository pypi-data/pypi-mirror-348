from pathlib import Path
from typing import List

from setuptools import find_packages, setup
from setuptools.dist import Distribution

from build_scripts.build_executables import build_executable


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


def get_platform_binaries() -> List[str]:
    """Get the list of binary files for the current platform."""
    bin_dir = Path("kusto_mcp/bin")
    if not bin_dir.exists():
        return []
    return [str(path.relative_to("kusto_mcp")) for path in bin_dir.glob("*")]


build_executable()

setup(
    name="kusto-mcp",
    # version is managed by setuptools_scm
    description="Kusto MCP (executables)",
    attrs={
        "author": "Microsoft Corporation",
    },
    readme="README.md",
    requires_python=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Development Status :: 2 - Pre-Alpha",
    ],
    packages=find_packages(),
    package_data={"kusto_mcp": get_platform_binaries()},
    entry_points={
        "console_scripts": [
            "kusto-mcp = kusto_mcp.launcher:run",
        ],
    },
    include_package_data=True,
    distclass=BinaryDistribution,
    zip_safe=False,
)

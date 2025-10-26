"""Setup script for mcp-generator."""

from setuptools import find_packages, setup

setup(
    name="mcp-generator",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "mcp_generator": ["templates/*.j2"],
    },
)

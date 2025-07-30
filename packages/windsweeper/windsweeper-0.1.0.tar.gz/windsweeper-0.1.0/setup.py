from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Get package version
with open(this_directory / "src" / "windsweeper" / "_version.py", "r", encoding="utf-8") as f:
    exec(f.read())

setup(
    name="windsweeper",
    version=__version__,  # noqa: F821
    author="Windsweeper Team",
    author_email="team@windsweeper.io",
    description="Python SDK for Windsweeper MCP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/windsweeper/windsweeper",
    project_urls={
        "Bug Tracker": "https://github.com/windsweeper/windsweeper/issues",
        "Documentation": "https://docs.windsweeper.io",
        "Source Code": "https://github.com/windsweeper/windsweeper",
        "Changelog": "https://github.com/windsweeper/windsweeper/blob/main/CHANGELOG.md",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "requests>=2.25.0,<3.0.0",
        "pydantic>=2.0.0,<3.0.0",
        "click>=8.0.0,<9.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "windsweeper=windsweeper.cli:main",
        ],
    },
)

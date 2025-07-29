from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="circheck",
    version="0.1.3",
    description="Static analysis tool to detect ZKP vulnerabilities in Circom circuits.",
    author="Dang Duong Minh Nhat",
    author_email="dangduongminhnhat2003@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "antlr4-python3-runtime"
    ],
    entry_points={
        'console_scripts': [
            'circheck = circheck.cli:main',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)

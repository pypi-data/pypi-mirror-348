from setuptools import setup, find_packages

setup(
    name="circheck",
    version="0.1.2",
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
)

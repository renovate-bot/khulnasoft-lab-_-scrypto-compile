"""
ScrytoCompile package installation
"""
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="scryto-compile",
    description="Util to facilitate smart contracts compilation.",
    url="https://github.com/khulnasoft-lab/scryto-compile",
    author="KhulnaSoft Lab",
    version="0.3.5",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["pycryptodome>=3.4.6", "cbor2", "solc-select>=v1.0.4", "toml>=0.10.2"],
    extras_require={
        "test": [
            "pytest",
            "pytest-cov",
        ],
        "lint": [
            "black==22.3.0",
            "pylint==2.13.4",
            "mypy==0.942",
            "darglint==1.8.0",
        ],
        "doc": [
            "pdoc",
        ],
        "dev": [
            "scryto-compile[test,doc,lint]",
        ],
    },
    license="AGPL-3.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"scryto_compile": ["py.typed"]},
    entry_points={"console_scripts": ["scryto-compile = scryto_compile.__main__:main"]},
)

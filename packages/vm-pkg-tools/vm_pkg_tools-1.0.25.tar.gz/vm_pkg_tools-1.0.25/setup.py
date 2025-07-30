from setuptools import setup, find_packages

# Reading the long description from the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vm-pkg-tools",
    version="1.0.25",
    author="Reza Barzegar Gashti",
    author_email="rezabarzegargashti@gmail.com",
    description="A private package for scout file parsing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/volleymateteam/scout_parser_py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="volleyball, parser, dvw, scout files",
    license="Proprietary",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "click>=8.1,<9.0",
        "pydantic>=2.0,<3.0",
        "sqlalchemy>=2.0,<3.0",
        "PyYAML>=6.0,<7.0",
        "unidecode>=1.3,<2.0",
        "chardet>=5.0,<6.0",
        "colorlog>=6.0,<7.0",
        "jsonschema>=4.0,<5.0",
    ],
    extras_require={
        "dev": [
            "setuptools>=65.5",
            "twine>=4.0.0",
            "black>=24.10",
            "flake8>=7.1",
            "isort>=5.13",
            "pylint>=3.3",
            "pytest>=8.3.4",
            "attrs>=24.3",
        ],
    },
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "vmtools-cli=vm_pkg_tools.core.main:main",
        ],
    },
)

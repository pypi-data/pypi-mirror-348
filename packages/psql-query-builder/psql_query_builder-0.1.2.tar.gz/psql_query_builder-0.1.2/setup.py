"""
Setup script for PSQL Query Builder.
"""

from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f.readlines() if line.strip()]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="psql-query-builder",
    version="0.1.2",
    author="Taha",  # Update with your actual name
    author_email="tahasamavati11@yahoo.com",  # Update with your actual email
    description="Generate PostgreSQL queries from natural language using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/celestialtaha/psql-query-builder",
    package_dir={"":"src"},  # Tell setuptools packages are under src
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "psql-query-builder=psql_query_builder.cli:main",
        ],
    },
    include_package_data=True,
)

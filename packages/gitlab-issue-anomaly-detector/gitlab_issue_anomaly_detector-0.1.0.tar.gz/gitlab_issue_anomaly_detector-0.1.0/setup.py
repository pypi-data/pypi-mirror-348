import os
from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="gitlab-issue-anomaly-detector",
    version="0.1.0",
    author="Author",
    author_email="author@example.com",
    description="GitLab issue anomaly detection and page generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/my-group-name2452611/my-project-name",
    packages=find_packages(include=["scripts", "scripts.*"]),
    include_package_data=True,
    package_data={
        "scripts": ["templates/*", "page_generator/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gitlab-anomaly-detector=scripts.main:main",
        ],
    },
)

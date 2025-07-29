from setuptools import setup, find_packages
import os
import sys


def get_requirements(path):
    with open(path) as f:
        return f.read().splitlines()


base_requirements = get_requirements(
    os.path.join("tms_integration", "requirements.txt")
)

# Define the requirements for each optional component
lis_winsped_requirements = get_requirements(
    os.path.join("tms_integration", "lis_winsped", "requirements.txt")
)
# Assuming carlo has its own requirements.txt
carlo_requirements = get_requirements(
    os.path.join("tms_integration", "carlo", "requirements.txt")
)

setup(
    name="tms_integration",
    version="0.1.0",
    description="A library for TMS integration",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(exclude=["tests*"]),
    install_requires=base_requirements,
    extras_require={
        "lis_winsped": lis_winsped_requirements,
        "carlo": carlo_requirements,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

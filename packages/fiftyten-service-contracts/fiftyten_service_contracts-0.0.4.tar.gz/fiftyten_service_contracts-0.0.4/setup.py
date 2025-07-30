from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fiftyten-service-contracts",
    version="0.0.4",
    author="FiftyTen",
    description="Shared type definitions and API contracts for FiftyTen microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/5010-dev/service-contracts",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "urllib3>=1.25.3",
        "python-dateutil",
    ],
)

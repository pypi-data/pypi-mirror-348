from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="clicksign_lib_v2",
    version="0.1.8",
    author="Giorgio Frigotto Lovatel",
    description="Consuming clicksign API V2 and making it available in lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["clicksign_lib_v2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[],
    dependency_links=["https://github.com/GiorgioFL15/clicksign_lib_v2"],
)

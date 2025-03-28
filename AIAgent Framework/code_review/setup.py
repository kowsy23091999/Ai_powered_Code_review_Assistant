from setuptools import setup, find_packages

setup(
    name="code_review",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "crewai>=0.100.1",
        "pyyaml>=6.0.1",
    ],
)

from setuptools import find_packages, setup

setup(
    name="pipelineDagster",
    packages=find_packages(exclude=["pipelineDagster_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "httpx", 
        "sqlalchemy", 
        "pandas",
        "numpy"  
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)

from setuptools import setup, find_packages

setup(
    name="r7kit",
    version="0.1",
    description="Task/workflow toolkit for Temporal + Redis",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(include=["r7kit", "r7kit.*"]),
    install_requires=[
        "temporalio>=1.0",
        "redis>=4.6",
        "pydantic>=2.0",
        "orjson>=3.9",
    ],
    python_requires=">=3.10",
)

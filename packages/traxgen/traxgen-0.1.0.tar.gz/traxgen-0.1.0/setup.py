from setuptools import setup, find_packages

setup(
    name="traxgen",  
    version="0.1.0",
    author="anonymous",  
    author_email="",
    description="Trajectory ground truth generator for agentic frameworks",
    packages=find_packages(include=["traxgen", "traxgen.*"]),
    install_requires=[
        "networkx>=2.8",
        "matplotlib>=3.5",
        "seaborn>=0.11",
        "pydantic>=1.10",
    ],
    python_requires=">=3.8",
)

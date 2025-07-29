from setuptools import setup, find_packages

setup(
    name="supplier_evaluator",
    version="0.1.0",
    description="Tool to evaluate supplier quotations based on price, delivery date, and quality.",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "pydantic",
        "crewai"
    ],
    python_requires=">=3.7",
)

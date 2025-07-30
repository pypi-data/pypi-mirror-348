from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="filter-persist",  # The name to install via pip
    version="0.1.2",         # 🚨 Increment this every release!
    description="Custom Streamlit AgGrid component",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Parshav Shivnani",
    packages=find_packages(),  # Automatically find all packages including 'filter_persist'
    include_package_data=True,
    install_requires=[
        "streamlit>=1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

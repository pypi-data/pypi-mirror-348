from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="filter-persist",
    version="0.1.4",
    description="Custom Streamlit AgGrid component",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Parshav Shivnani",
    packages=find_packages(),   # Finds 'filter_persist'
    package_data={
        "filter_persist": ["frontend/build/**/*"],
    },
    include_package_data=True,
    install_requires=[
        "streamlit>=1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

from setuptools import setup, find_packages

setup(
    name="filter-persist",  # your package name here
    version="0.1.0",
    description="Custom Streamlit AgGrid component",
    author="Parshav Shivnani",
    packages=["filter_persist"], # Package folder name with underscore
    include_package_data=True,
    install_requires=[
        "streamlit>=1.0",
    ],
    package_data={
        "my_component": ["frontend/build/**/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

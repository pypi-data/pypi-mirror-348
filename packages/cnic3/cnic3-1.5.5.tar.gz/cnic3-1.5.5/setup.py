from setuptools import setup, find_packages

setup(
    name="cnic3",
    version="1.5.5",
    author="cnic3",
    description="Advanced data loader and preprocessor for CSV and Parquet files",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=["pandas>=1.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)

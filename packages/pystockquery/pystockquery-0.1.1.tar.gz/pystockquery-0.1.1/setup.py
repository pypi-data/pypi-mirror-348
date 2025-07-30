from setuptools import setup, find_packages

setup(
    name="pystockquery",
    version="0.1.1",
    description="A powerful stock screening and analysis tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="PredictRAM",
    author_email="support@predictram.com",
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0',
        'openpyxl>=3.0',
        'matplotlib>=3.0',
        'seaborn>=0.11',
        'numpy>=1.0'
    ],
    include_package_data=True,
    package_data={
        'pystockparameter': ['data/*.xlsx'],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pystock=pystockparameter.cli:main',
        ],
    },
)
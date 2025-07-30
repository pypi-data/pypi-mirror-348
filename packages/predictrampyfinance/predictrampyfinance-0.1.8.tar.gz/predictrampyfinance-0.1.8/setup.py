from setuptools import setup, find_packages
from pathlib import Path

# Load README.md for long_description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='predictrampyfinance',
    version='0.1.8',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    description='Access prepackaged stock-level financial data (JSON) via a simple Python API.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # ← important for Markdown rendering!
    author='PredictRAM Data',
    author_email='support@predictram.com',
    url='https://pypi.org/project/predictrampyfinance',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)

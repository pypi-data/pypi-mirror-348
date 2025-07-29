from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='mymathlib_test',
    version='0.4',
    description='A simple math operations library for demo purposes',
    author='nani123',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    author_email='nanireddy8898@gmail.com',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    license_files = "MIT",

)

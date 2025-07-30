from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='krippendorrf-graph',
    version='0.2.1',
    description='A Python package for computing krippendorrfs alpha for graph (modified from https://github.com/grrrr/krippendorff-alpha/blob/master/krippendorff_alpha.py)',
    url='https://github.com/junbohuang/Krippendorrf-alpha-for-graph',
    author='Junbo Huang',
    author_email='junbo.huang@uni-hamburg.de',
    license='Apache 2 License',
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=["krippendorrf_graph"]
)

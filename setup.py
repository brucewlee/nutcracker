from distutils.core import setup
from setuptools import find_packages
# python setup.py sdist
# python -m twine upload dist/*
# pip install -e .
setup(
    name = 'nutcracker',  
    version='0.0.1a7',
    description = 'In Development',
    author = 'Bruce W. Lee',
    author_email = 'bruce@walnutresearch.com', 
    packages=find_packages(),
    keywords='Evaluation',
    install_requires=[
          'pyyaml>=6.0.1',
          'openai>=1.10.0'
      ],
    include_package_data=True,
    package_data={'nutcracker': ['*']}
)
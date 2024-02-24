from distutils.core import setup
from setuptools import find_packages
# python setup.py sdist
# python -m twine upload dist/*
# pip install -e .
# git tag -a "0.0.1a12" -m "pypi workflow revamp"
# git push --tags    
setup(
    name = 'nutcracker-py',  
    version='{{VERSION_PLACEHOLDER}}',
    description = 'streamline LLM evaluation',
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
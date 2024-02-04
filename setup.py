from distutils.core import setup
from setuptools import find_packages
# python setup.py sdist
# python -m twine upload dist/*
setup(
    name = 'nutcracker',  
    version='a-1.0.0',
    description = 'In Development',
    author = 'Bruce W. Lee',
    author_email = 'bruce@walnutresearch.com', 
    packages=find_packages(),
    keywords='Evaluation',
    install_requires=[
          'huggingface_hub>=0.19.4',
          'litellm>=1.11.0',
          'pyyaml>=6.0.1',
          'openai>=1.10.0'
      ],
    include_package_data=True,
    package_data={'': ['*']}
)
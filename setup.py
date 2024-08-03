from distutils.core import setup
from setuptools import find_packages

this_version='0.0.2a02'

# python setup.py sdist
# python -m twine upload dist/*
# pip install -e .
# git tag -a "0.0.1a12" -m "pypi workflow revamp"
# git push --tags   

# pip install pipreqs
# pipreqs .
setup(
    name = 'nutcracker-py',  
    version=this_version,
    setup_requires="setupmeta",
    description = 'streamline LLM evaluation',
    author = 'Bruce W. Lee',
    author_email = 'bruce@walnutresearch.com', 
    packages=find_packages(),
    keywords='Evaluation',
    install_requires=[
        'anthropic==0.26.1','boto3==1.34.115','botocore==1.29.76','cohere==5.5.3','numpy==1.24.3','openai==1.30.4','pytest==7.4.0','PyYAML==6.0.1','Requests==2.32.3','setuptools==68.0.0','tqdm==4.65.0'
      ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={'': ['*']}
)
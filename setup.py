from setuptools import setup, find_packages
import subprocess

def _get_version_hash():
  """Talk to git and find out the tag/hash of our latest commit"""
    try:
        p = subprocess.Popen(["git", "describe",
                                "--tags", "--dirty", "--always"],
                                stdout=subprocess.PIPE)
    except EnvironmentError:
        print("Couldn't run git to get a version number for setup.py")
        return None
    ver = p.communicate()[0]
    return ver.strip()

# python setup.py sdist
# python -m twine upload dist/*
# pip install -e .
# git tag -a "0.0.1a12" -m "pypi workflow revamp"
# git push --tags    
setup(
    name = 'nutcracker-py',  
    version=_get_version_hash(),
    setup_requires="setupmeta",
    description = 'streamline LLM evaluation',
    author = 'Bruce W. Lee',
    author_email = 'bruce@walnutresearch.com', 
    packages=find_packages(),
    keywords='Evaluation',
    install_requires=[
          'pyyaml>=6.0.1',
          'openai>=1.10.0'
      ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={'nutcracker': ['*']}
)
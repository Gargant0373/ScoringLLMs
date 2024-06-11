# setup.py
from setuptools import setup, find_packages

def get_requirements(path: str):
    return [l.strip() for l in open(path)]

setup(
    name='ScoringLLMs',
    version='0.1.0',
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)

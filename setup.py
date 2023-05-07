from setuptools import setup

setup(
    name='pipcheck',
    version='0.1.0',
    description='This is a python3 program that checks if the libraries in the requirements.txt file are up to date.',
    author='Bapth',
    author_email='py-bapth@gmail.com',
    packages=['pipcheck'],
    install_requires=['requests', 'beautifulsoup4'],
)

#! /usr/bin/env python
from setuptools import setup

descr = """
    Conditional Random Field Parser for MEDLINE and
    Pubmed Open-Access affiliation string
"""

if __name__ == "__main__":
    setup(
        name='affilparser',
        packages=['affilparser'],
        include_package_data=True,
        version='0.1',
        description='Python CRF parser for MEDLINE and Pubmed Open-Access affiliation string',
        long_description=open('README.md').read(),
        url='https://github.com/titipata/affilparser',
        author='Titipat Achakulvisut, Daniel Acuna',
        author_email='my.titipat@gmail.com',
        license='(c) 2017 Titipat Achakulvisut',
        keywords='parser, affilation',
        install_requires=['numpy', 'pandas', 'spacy', 'python-crfsuite'],
        classifiers=[
            'Development Status :: 3 - Alpha'
        ],
    )

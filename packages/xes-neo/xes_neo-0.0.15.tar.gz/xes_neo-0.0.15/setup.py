# coding: utf-8
from __future__ import print_function, unicode_literals
import sys
import codecs
from setuptools import setup, find_packages
from xes_neo._version import __version__, __author__, __email__



def long_description():
    with codecs.open('README.md', 'rb') as readme:
        if not sys.version_info < (3, 0, 0):
            return readme.read().decode('utf-8')


setup(
    name='xes_neo',
    version=__version__,
    packages=find_packages(),

    author=__author__,
    author_email=__email__,
    keywords=['GA', 'XES','analysis'],
    description='XES Analysis using GA',
    long_description=long_description(),
    url='https://github.com/lanl/XES_Neo_Public.git',
    download_url='https://github.com/lanl/XES_Neo_Public/tarball/main',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'numpy',
        'attrs',
        'matplotlib',
        'scipy',
        'psutil'
    ],
    entry_points={
        'console_scripts': [
            'xes_neo = xes_neo.xes:main',
            'xes_neo_gui = xes_neo.gui.xes_neo_gui:main',
        ]
    },
    license='GPLv3',
)

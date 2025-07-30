from setuptools import setup, find_packages

VERSION = '0.0.19'
DESCRIPTION = 'A collection of Python functions for structural engineering'
LONG_DESCRIPTION = 'This package contains random utility functions accrued over many years of structural engineering research and teaching'

setup(
	name = 'bennycloth',
	version = VERSION,
	author = 'Michael H. Scott',
	author_email = 'mhscott@oregonstate.edu',
	description = DESCRIPTION,
	long_description = LONG_DESCRIPTION,
	packages = find_packages(),
	install_requires = ['requests'],
	keywords = ['python','opensees'],
	classifiers = ['Programming Language :: Python :: 3',
		'Operating System :: OS Independent'
	],
	python_requires = '>=3.6'
)

from setuptools import setup, find_packages
import sys, os

VERSION = '0.3.0-alpha'

setup(name='virtstrap-local',
    version=VERSION,
    description="",
    long_description="""\
""",
    classifiers=[],
    keywords='',
    author='Reuven V. Gonzales',
    author_email='reuven@tobetter.us',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'virtstrap-core',
    ],
    entry_points={
        'console_scripts': [
            'virtstrap-local = virtstrap_local.runner:main'
        ]
    },
)

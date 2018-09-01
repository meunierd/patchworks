from setuptools import setup

setup(
    name='patchworks',
    entry_points={
        'console_scripts': [
            'patchworks = patchworks.cli:cli'
        ]
    }
)

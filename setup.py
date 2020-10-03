from setuptools import setup

# from https://packaging.python.org/guides/making-a-pypi-friendly-readme/
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='undocker',
        author = 'Lars Kellogg-Stedman',
        author_email = 'lars@oddbit.com',
        version='7',
        description='Unpack docker images',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='http://github.com/larsks/undocker',
        py_modules=['undocker'],
        entry_points={
            'console_scripts': [
                'undocker = undocker:main',
                ],
            }
        )

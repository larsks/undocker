from setuptools import setup

setup(name='undocker',
        author = 'Lars Kellogg-Stedman',
        author_email = 'lars@oddbit.com',
        version='6',
        description='Unpack docker images',
        url='http://github.com/larsks/undocker',
        py_modules=['undocker'],
        entry_points={
            'console_scripts': [
                'undocker = undocker:main',
                ],
            }
        )

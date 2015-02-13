from setuptools import setup, find_packages

with open('requirements.txt') as fd:
    setup(name='undocker',
          version='3',
          py_modules=['undocker'],
          entry_points={
              'console_scripts': [
                  'undocker = undocker:main',
              ],
          }
          )

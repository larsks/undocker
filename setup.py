from setuptools import setup, find_packages

with open('requirements.txt') as fd:
    setup(name='undocker',
          version='1',
          py_modules=['undocker.py'],
          entry_points={
              'console_scripts': [
                  'undocker = undocker:main',
              ],
          }
          )

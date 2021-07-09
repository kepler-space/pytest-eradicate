import os

# this is expected to fail when running pytest --eradicate setup.py
# 1 == 1

from setuptools import setup

if __name__ == "__main__":
    setup(
        name='pytest-eradicate',
        description='pytest plugin to check for commented out code',
        long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
        license="MIT license",
        version='0.0.5',
        author='Johan Bloemberg',
        author_email='github@ijohan.nl',
        url='https://github.com/aequitas/pytest-eradicate',
        py_modules=['pytest_eradicate'],
        entry_points={'pytest11': ['eradicate = pytest_eradicate']},
        install_requires=['pytest-cache', 'pytest>=2.4.2', 'eradicate', ],
        classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.8',
        ],
    )

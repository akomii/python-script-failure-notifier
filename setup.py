# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='YourProjectName',
    version='1.0.0',
    author='Your Name',
    author_email='your@email.com',
    description='A brief description of your project',
    url='https://github.com/yourusername/yourprojectname',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'your_script_name=your_package.module:main',
        ],
    },
)

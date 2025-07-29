# setup.py

from setuptools import setup, find_packages

setup(
    name='frameworkjs',
    version='0.1.0',
    author='Your Name',
    description='Reusable Selenium BasePage for Pytest automation',
    packages=find_packages(),
    install_requires=[
        'selenium>=4.0.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Pytest",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

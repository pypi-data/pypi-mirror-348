from setuptools import setup, find_packages

setup(
    name='ts-viz',
    version='0.1.0',
    description='Time Series Visualization Tools',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'seaborn',
        'numpy',
    ],
    python_requires='>=3.11',
)

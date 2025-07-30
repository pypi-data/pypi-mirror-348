from setuptools import setup, find_packages

setup(
    name='kasturing_testing_lib',
    version='1.0.4',
    description='A helpful library for setting up data collection for the ML pipeline',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rohit Raj',
    url='https://github.com/RohitRaj654487/kasturing_lib',
    license='Apache Software License 2.0',
    packages=find_packages(),
    python_requires='>=3.7',
)
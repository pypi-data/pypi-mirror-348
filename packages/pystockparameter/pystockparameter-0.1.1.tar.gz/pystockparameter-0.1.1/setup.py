from setuptools import setup, find_packages

setup(
    name='pystockparameter',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'openpyxl'
    ],
    author='PredictRAM',
    author_email='support@predictram.com',
    description='Python package to fetch stock data from a merged Excel file',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pystockparameter',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)

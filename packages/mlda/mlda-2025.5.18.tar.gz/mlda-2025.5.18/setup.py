from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='mlda',  # required
    version='2025.5.18',
    description='mlda: A Python package for Machine Learning-base Data Assimilation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Feng Zhu',
    author_email='fengzhu@ucar.edu',
    url='https://github.com/fzhu2e/mlda',
    packages=find_packages(),
    include_package_data=True,
    license='BSD-3',
    zip_safe=False,
    keywords=['Machine Learning', 'Data Assimilation'],
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires=[
        'netCDF4',
        'xarray',
        'dask',
        'nc-time-axis',
        'colorama',
        'tqdm',
        'x4c-exp',
    ],
)

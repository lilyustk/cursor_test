from setuptools import setup, find_packages

setup(
    name="cursor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'dash',
        'dash-bootstrap-components',
        'pandas',
        'plotly',
        'numpy'
    ],
) 
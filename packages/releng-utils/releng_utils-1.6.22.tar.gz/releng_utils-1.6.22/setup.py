from setuptools import setup, find_packages


long_description = """
releng-utils is a lightweight and modular Python library designed to streamline 
and automate common tasks in release engineering workflows.

The library includes helpers for version normalization, Git tagging, semantic 
versioning enforcement, build artifact handling, changelog templating, environment 
consistency checks, and integration hooks for CI/CD pipelines.

Ideal for developers, DevOps engineers, and release managers, releng-utils helps 
reduce manual effort and minimize release errors by standardizing release 
engineering practices in Python-based projects.
"""

setup(
    name='releng-utils',
    version='1.6.22',
    packages=find_packages(),
    description='releng-utils',
    long_description_content_type='text/plain',
    long_description=long_description,
    url='https://github.com/opnfv/releng-utils',
    download_url='https://github.com/opnfv/releng-utils',
    project_urls={
        'Documentation': 'https://github.com/opnfv/releng-utils'},
    author='Baxter Rogers',
    author_email='baxpr@vu1.org',
    python_requires='>=3.8',
    platforms=['Linux'],
    license='GNU',
    install_requires=[
        'requests',
        'pylint',
        'cpjson',
        'loguru'
    ],

)

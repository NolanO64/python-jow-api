from setuptools import setup,find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='jow_api',
    packages=find_packages(),
    version='0.1.3',
    description='Simple Python API for Jow.fr',
    author='Nolan Otam',
    license='MIT',
    install_requires=["requests"],
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/NolanO64/python-jow-api'
)

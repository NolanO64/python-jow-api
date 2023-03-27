from setuptools import setup,find_packages

setup(
    name='jow_api',
    packages=find_packages(),
    version='0.1.0',
    description='Simple Python API for Jow.fr',
    author='Nolan Otam',
    license='MIT',
    install_requires=["requests"]
)
from setuptools import setup, find_packages

setup(
    name='apigle',
    version='1.0.0',
    description='Official Python client for Apigle.com API',
    author='Boztek LTD',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    python_requires='>=3.7',
)

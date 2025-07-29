from setuptools import setup, find_packages

setup(
    name="schemaplus-shopify-utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
)
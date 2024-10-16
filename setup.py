from setuptools import setup, find_packages

setup(
    name='SessionHandler',
    version='1.0',
    description='',
    packages=find_packages(),  # Include sub-folders
    install_requires=[

    ],
    include_package_data=True,  # Important for non-code files like images
)
from setuptools import setup, find_packages

setup(
    name="voiceflow-module",
    version="0.4.3",
    author="Alex",
    author_email="Alex@parnidia.com",
    description="Module to help you with knowledge base management",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://parnidia.com",
    packages=find_packages(),
    classifiers=[                      # Metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "xmltodict",
        "tiktoken"
    ],
)

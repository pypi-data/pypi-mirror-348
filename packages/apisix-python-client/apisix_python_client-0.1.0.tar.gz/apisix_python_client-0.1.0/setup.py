from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="apisix-python-client",
    version="0.1.0",
    author="Belhachemi Youcef",
    author_email="belhachemi.youcef@gmail.com",
    description="A  Python client for Apache APISIX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sifoo-31/apisix-python-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
)
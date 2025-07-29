from setuptools import setup, find_packages

setup(
    name="base58uuid",
    version="0.1.0",
    packages=find_packages(),
    description="A tiny, zero-dependency Python library for generating and converting UUIDs to Base58-encoded strings",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Yoshitake Hatada",
    author_email="yhatada@gingdang.co.jp",
    url="https://github.com/htpboost/base58uuid",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
) 
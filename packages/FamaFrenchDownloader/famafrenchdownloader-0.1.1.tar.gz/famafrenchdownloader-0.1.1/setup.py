from setuptools import setup, find_packages

setup(
    name="FamaFrenchDownloader",
    version="0.1.1",
    description="A Python library to easly download Fama-French Factor data for various regions and factor models (3-factors, 5-factors, Momentum).",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Francesco Finardi",
    author_email="finardfr@gmail.com",  # optional
    url="https://github.com/finardfr/FamaFrenchDownloader",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0",
        "requests>=2.0"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    license="MIT",
)
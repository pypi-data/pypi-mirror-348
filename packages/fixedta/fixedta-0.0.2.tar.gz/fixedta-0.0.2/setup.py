# -*- coding: utf-8 -*-
from distutils.core import setup

long_description = "Fixed version of pandas-ta"
setup(
    name="fixedta",
    packages=[
        "fixedta",
        "fixedta.candles",
        "fixedta.cycles",
        "fixedta.momentum",
        "fixedta.overlap",
        "fixedta.performance",
        "fixedta.statistics",
        "fixedta.trend",
        "fixedta.utils",
        "fixedta.utils.data",
        "fixedta.volatility",
        "fixedta.volume"
    ],
    version=".".join(("0", "0", "2")),
    description=long_description,
    long_description=long_description,
    author="Husain Chhil",
    author_email="hychhil@gmail.com",
    url="https://www.google.com",
    maintainer="Husain Chhil",
    maintainer_email="hychhil@gmail.com",
    download_url="https://www.google.com",
    keywords=["technical analysis", "trading", "python3", "pandas"],
    license="The MIT License (MIT)",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    package_data={
        "data": ["data/*.csv"],
    },
    install_requires=["pandas"],
    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require={
        "dev": [
            "alphaVantage-api", "matplotlib", "mplfinance", "scipy",
            "sklearn", "statsmodels", "stochastic",
            "talib", "tqdm", "vectorbt", "yfinance",
        ],
        "test": ["ta-lib"],
    },
)


# to build the package:
# python setup.py sdist
# to install the package:
# python setup.py install
# to build the package:

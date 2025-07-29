from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="blbr-scripts",
    version="0.1.0",
    description="BLBR Research Scripts for financial data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="BLBR Research Team",
    author_email="info@blbr-research.com",
    url="https://github.com/blbr-research/blbr-scripts",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "blbr_scripts": ["data/**/*", "*.py"],
    },
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'blbr-run-step=blbr_scripts.run_step:main',
            'blbr-dhan-ohlc=blbr_scripts.dhan_ohlc_to_file:main',
            'blbr-dhan-mongodb=blbr_scripts.dhan_ohlc_to_mongodb:main',
            'blbr-tvdatafeed=blbr_scripts.tvdatafeed_ohlcv:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='finance, trading, data analysis, stock market',
)

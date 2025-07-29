from setuptools import setup, find_packages

setup(
    name="breeze-historical",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "breeze-connect",
        "boto3",
        "requests",
        "python-dotenv",
        "flask",
        "selenium",
        "webdriver-manager",
        "pyotp"
    ],
    package_data={
        'breeze_historical': ['symbol_map.json'],
    },
    author="Kunal Agarwal",
    author_email="kunalagarwal3535@gmail.com",
    description="A library for fetching and caching historical market data from Breeze API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kunalAgarwal35/building_breeze_wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 
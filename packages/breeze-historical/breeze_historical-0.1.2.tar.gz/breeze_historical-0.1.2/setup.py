from setuptools import setup, find_packages

setup(
    name="breeze-historical",
    version="0.1.2",
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
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for fetching and caching historical market data from Breeze API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/breeze-historical",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 
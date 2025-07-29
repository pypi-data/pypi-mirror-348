from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ukraine-phone-formatter",
    version="0.1.0",
    author="Andrii Stavskyi",
    author_email="an.stawski@outlook.com",
    description="Ukraine Phone Formatter is a simple Python library that formats Ukrainian phone numbers into a readable and standardized format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stkossman/ukraine_phone_formatter_py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
from setuptools import setup, find_packages

setup(
    name="simplinear_regression",
    version="0.1.0",
    author="Md. Ismiel Hossen Abir",
    author_email="ismielabir1971@gmail.com",
    description="A simple Linear Regression implementation in pure Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
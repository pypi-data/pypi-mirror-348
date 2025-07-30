from setuptools import setup, find_packages

setup(
    name="pypaint-by-anagh",

    version="0.1.0",
    description="A simple Python package to draw shapes with turtle graphics.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="anaghbarnwal@hotmail.com",
    
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

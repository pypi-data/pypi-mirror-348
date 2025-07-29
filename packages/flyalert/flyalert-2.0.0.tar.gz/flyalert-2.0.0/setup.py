from setuptools import setup, find_packages

setup(
    name="flyalert",
    version="2.0.0",
    description="Custom animated alerts and dialogs for PyQt5.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Amirhossein Bohlouli",
    author_email="bohloli.amirh@gmail.com",
    url="https://github.com/Amirhossein871/flyalert",
    packages=find_packages(),
    install_requires=[
        "PyQt5"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

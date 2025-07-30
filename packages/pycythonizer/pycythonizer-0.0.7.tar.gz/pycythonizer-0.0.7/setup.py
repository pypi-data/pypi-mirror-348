from setuptools import setup, find_packages


setup(
    name="pycythonizer",
    version="0.0.7",
    author="scarredknight",
    author_email="boazmaroko123@gmail.com",
    description="A tool to compile python files into Cython binaries",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Boaz-Maroko/cython_compiler",

    packages=find_packages(),
    install_requires=["cython>=3.1.0", "click", "setuptools"],
    entry_points={
        "console_scripts": ["pycythonizer=pycythonizer.cli:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7"
)
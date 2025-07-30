from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name="ansiformatter",
    version="0.1.0",
    author="Quillai Mohammed Eisa",
    author_email="quillai20011114@gmail.com",
    description="A package for formatting text in terminal using ANSI in Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/quillaiMohammed/ansi-formatter",
    packages=find_packages(),
    python_requires='>=3.9',
    ext_modules=cythonize(
        ["ansiformatter/*.pyx"],
        compiler_directives={"language_level": "3"}
    ),
    zip_safe=False,
)

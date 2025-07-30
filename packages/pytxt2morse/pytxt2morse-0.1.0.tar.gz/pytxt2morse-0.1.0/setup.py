from setuptools import setup, find_packages

setup(
    name="pytxt2morse",
    version="0.1.0",
    description="Convert text to Morse code and Morse code to text.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Md. Ismiel Hossen Abir",
    author_email="ismielabir1971@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)
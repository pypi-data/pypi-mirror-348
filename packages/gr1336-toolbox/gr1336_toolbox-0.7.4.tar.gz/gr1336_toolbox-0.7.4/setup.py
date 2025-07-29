from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    version="0.7.4",
    name="gr1336_toolbox",
    description="Personal collection of tools for any python projects. Currently in Pre-Alpha, many resources will be added, removed, and modified until everything aligns with most common needs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gr1336/gr1336_toolbox/",
    install_requires=[
        "markdownify>=0.12.1",
        "markdown2>=2.4.13",
        "pyperclip>=1.8.2",
        "textblob>=0.18.0",
        "pyyaml>=6.0.0",
        "nltk",
        "scikit-learn>=1.4.0",
        "gruut",
        "num2words"
    ],
    author="gr1336",
    license="Apache Software License (Apache-2.0)",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Utilities",
    ],
)

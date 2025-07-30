import setuptools
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UzbekTagger",
    version="0.0.9",
    author="Maksud Sharipov, Ollabergan Yuldashov",
    author_email="maqsbek72@gmail.com, ollaberganyuldashov@gmail.com",
    description="Part of Speech Tagger for Uzbek Language.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaksudSharipov/UzbekTagger",
    project_urls={
        "Bug Tracker": "https://github.com/MaksudSharipov/UzbekTagger/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['python', 'UzbekTagger', 'uzbek texts', 'Tagger','POS','Part of Speech'],
    package_dir={"": "src"},
    packages=find_packages(where="src"),

    install_requires=[
        "nltk>=3.5",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={"": ["*.xml"]},

    #package_data={"": ["cyr_exwords.csv", "lat_exwords.csv"],},
)
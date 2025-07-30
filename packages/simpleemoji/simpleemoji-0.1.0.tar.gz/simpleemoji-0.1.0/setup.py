from setuptools import setup, find_packages

setup(
    name="simpleemoji",
    version="0.1.0",
    author="Dextro",
    author_email="levovarma@gmail.com",
    description="A tiny package to get some simple emojis in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

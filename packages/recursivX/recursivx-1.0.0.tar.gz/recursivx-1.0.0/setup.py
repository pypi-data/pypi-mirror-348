from setuptools import setup, find_packages

setup(
    name="recursivX",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "recursivX=recursivX.recursivX:main"
        ]
    },
    author="Paul Smith",
    description="Recursive archive extractor with password detection",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Paul00/recursivX",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
)

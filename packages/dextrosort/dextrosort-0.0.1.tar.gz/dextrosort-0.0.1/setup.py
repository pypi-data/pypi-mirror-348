from setuptools import setup, find_packages

setup(
    name="dextrosort",
    version="0.0.1",
    author="M Vashishta Varma",
    author_email="levovarma@gmail.com",
    description="A simple and efficient merge sort implementation using divide-and-conquer.",
    long_description=open("README.txt").read() + '\n\n' + open("CHANGELOG.txt").read(),
    long_description_content_type="text/markdown",
    url="",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords="dextrosort",
    python_requires=">=3.6",
)

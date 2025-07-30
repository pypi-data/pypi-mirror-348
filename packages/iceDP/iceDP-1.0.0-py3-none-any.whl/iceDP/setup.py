import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="density-peak-for-hic",
    version="0.0.1",
    description="Read the latest Real Python tutorials",
    long_description=README,
    long_description_content_type="text/markdown",
    #url="https://github.com/realpython/reader",
    author="RH Chen",
    author_email="chen_ruhai@gibh.ac.cn",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["densityPeak"], #packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["pandas", "numpy", "math", "multiprocessing", "functools", "scipy"],

    #entry_points={
#        "console_scripts": [
#            "realpython=reader.__main__:main",
#        ]
#    },
)


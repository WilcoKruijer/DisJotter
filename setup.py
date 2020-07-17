import setuptools
import os
from shutil import copyfile


short_desc = "FAIR-Cells allows the user to interactively create a Docker image from a Jupyter Notebook."

try:
    with open("./README.md", "r") as rm:
        long_description = rm.read()
except FileNotFoundError:
    long_description = short_desc


setuptools.setup(
    name="FAIR-Cells",
    version="1.0.4",
    author="Wilco Kruijer, S. Koulouzis",
    author_email="wilcokruijer@gmail.com, S.Koulouzis@uva.nl",
    description=short_desc,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QCDIS/FAIRCells",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "docker>=4.2.0",
        "pigar>=0.10.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

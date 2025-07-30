from setuptools import setup, find_packages
import re


# Version number
verstrline = open('shpg/_version.py', "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version in shpg/_version.py")


setup(
    name='shpg',
    version=version,
    packages=find_packages(),
    description='Create static HTML pages.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    author="Bastien Cagna",
    license='BSD 3',
    
    install_require=[],
    extras_require={
        "doc": ["sphinx>=" + '1.0', "furo", "sphinx_design"],
        "dev": ["pytest", "build", "twine"]
    },
    include_package_data=True
)

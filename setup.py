from setuptools import setup

import hooker

setup(
    name=hooker.__name__,
    description=hooker.__desc__,
    version=hooker.__version__,

    author="Satori-NG org",
    author_email=hooker.__email__,

    packages=["hooker"],
)

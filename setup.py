from pypandoc import convert
from setuptools import setup

import hooker


def read_md(name):
    # Hack to pass the "rst_lint.py" - PyPI
    return convert(name, "rst").replace("~", "^")


try:
    LONG_DESCRIPTION = read_md("README.md")
except IOError:
    LONG_DESCRIPTION = hooker.__github__ + "/blob/master/README.md"

if not hasattr(hooker, "__version__"):
    hooker.__version__ = "develop"


setup(
    name=hooker.__name__,
    description=hooker.__desc__,
    long_description=LONG_DESCRIPTION,
    version=hooker.__version__,

    author="Satori-NG org",
    author_email=hooker.__email__,

    url=hooker.__github__,

    packages=["hooker"],
    keywords=["hook", "event", "plugin", "extension", "module"]
)

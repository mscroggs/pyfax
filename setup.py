import os
import sys
import setuptools

if sys.version_info < (3, 6):
    print("Python 3.6 or higher required, please upgrade.")
    sys.exit(1)

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md")) as f:
    long_description = f.read()

if __name__ == "__main__":
    setuptools.setup(
        name="pyfax",
        description="a Python library for generating teletext tti files",
        long_description=long_description,
        long_description_content_type="text/markdown",
        version="2022.6.2",
        author="Matthew Scroggs",
        license="MIT",
        author_email="pyfax@mscroggs.co.uk",
        maintainer_email="pyfax@mscroggs.co.uk",
        url="https://github.com/mscroggs/pyfax",
        packages=["pyfax", "pyfax.tools"],
        install_requires=["requests", "feedparser"],
        extras_require={
          "ci": ["pytest"]
        }
    )

from setuptools import setup


def get_version() -> str:
    version: dict[str, str] = {"__name__": "__not_main__"}
    with open("parapara/version.py") as fp:
        exec(fp.read(), version)

    return version["__version__"]


DESCRIPTION = (
    "parapara-anime: This is a helper for creating a movie of a series of images."
)
NAME = "parapara-anime"
AUTHOR = "siruku6"
AUTHOR_EMAIL = "sirukufarios@gmail.com"
URL = "https://github.com/siruku6/parapara-anime"
LICENSE = "MIT License"
DOWNLOAD_URL = "https://github.com/siruku6/parapara-anime"
VERSION = get_version()
PYTHON_REQUIRES = ">=3.8"

INSTALL_REQUIRES = [
    "IPython>=7.23.1",
    "matplotlib>=3.0.0",
    "numpy>=1.15",
    "pyvirtualdisplay>=3.0",
    "tqdm>=4.66.0",
]
EXTRAS_REQUIRE = {
    "tutorial": [],
}
TEST_REQUIRES = [
    "pytest>=3",
]

PACKAGES = ["parapara"]

CLASSIFIERS = [
    # NOTE: Refer to this link, https://e-tec-memo.herokuapp.com/article/177/
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Framework :: Matplotlib",
]

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url=URL,
    version=VERSION,
    download_url=DOWNLOAD_URL,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    tests_require=TEST_REQUIRES,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
)

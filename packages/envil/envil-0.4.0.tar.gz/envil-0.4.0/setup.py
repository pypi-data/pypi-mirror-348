from setuptools import setup

# https://setuptools.readthedocs.io/en/latest/
setup(
    name="envil",
    version="0.4.0",
    description="Get non-string values from environment variables.",
    long_description=open("README.md", "rt").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/luismsgomes/envil",
    author="Luís Gomes",
    author_email="luismsgomes@gmail.com",
    license="GPLv3",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="util",
    install_requires=[],
    package_dir={"": "src"},
    py_modules=["envil"],
)

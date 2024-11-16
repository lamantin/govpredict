#setup.py
from setuptools import setup, find_packages
setup(
    name = "fara_foreign_principals",
    version = "0.1",
    author = "Stv@n",
    author_email="istvan.makai@gmail.com",
    license="bsd",
    description="a little scrapy crawler what can collapse fara foreign principals data as json",
    packages = find_packages(),
    entry_points = {'scrapy': ['settings = fara_foreign_principals.settings']},
    )
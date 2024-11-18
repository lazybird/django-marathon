import os

from setuptools import find_packages, setup

import marathon


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""


setup(
    name="django-marathon",
    version=marathon.__version__,
    description=read("DESCRIPTION"),
    long_description=read("README.rst"),
    long_description_content_type='text/x-rst',
    keywords="Django single runner tasks concurrency concurrency-avoidance",
    packages=find_packages(),
    author="",
    author_email="",
    url="https://github.com/lazybird/django-marathon/",
    include_package_data=True,
)

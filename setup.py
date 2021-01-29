#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Flask==1.1.2",
    "Flask-Login==0.5.0",
    "Flask-OAuthlib==0.9.6",
    "facebook-sdk==3.1.0",
    "httplib2==0.18.1",
    "apiclient==1.0.4",
    "oauth2client==4.1.3",
    "google-api-python-client==1.12.8",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Pyunghyuk Yoo",
    author_email="yoophi@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="OAuth Provider integration for Flask-Login",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="flask_social_login",
    name="flask_social_login",
    packages=find_packages(include=["flask_social_login", "flask_social_login.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/yoophi/flask_social_login",
    version="0.2.1",
    zip_safe=False,
)

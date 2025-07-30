#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="interaction-logger",
    version="0.3.3",
    author="Josphat-n",
    author_email="josphatnjoroge254@gmail.com",
    description="A package for logging user interactions with a django distributed system.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6.3",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["django", "logging", "user activity", "audit trail", "monitoring"],
    packages=["interaction_logger"],
    include_package_data=True,
    install_requires=[
        "Django==3.0.8",
        "asgiref>=3.4.1",
        "backports.zoneinfo>=0.2.1; python_version<'3.9'",
        "pytz>=2025.2",
        "sqlparse>=0.4.4",
    ],
    package_data={
        "interaction_logger": ["migrations/*.py", "templates/*.html", "static/*"],
    },
)

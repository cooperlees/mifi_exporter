#!/usr/bin/env python3

from setuptools import setup


ptr_params = {
    "entry_point_module": "me",
    "test_suite": "me_tests",
    "test_suite_timeout": 60,
    "required_coverage": {
        "me.py": 25,
    },
    "run_black": True,
    "run_flake8": True,
    "run_mypy": True,
    "run_usort": True,
}


setup(
    name="mifi_exporter",
    version="2021.6.14",
    description=("asyncio MIFI prometheus exporter"),
    py_modules=["me", "me_tests"],
    url="http://github.com/cooperlees/mifi_exporter/",
    author="Cooper Lees",
    author_email="me@cooperlees.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 3 - Alpha",
    ],
    entry_points={"console_scripts": ["mifi-exporter = me:main"]},
    install_requires=["aioprometheus[aiohttp]", "click"],
    extras_require={
        "test": ["ptr"],
    },
    python_requires=">=3.8",
    test_suite=ptr_params["test_suite"],
)

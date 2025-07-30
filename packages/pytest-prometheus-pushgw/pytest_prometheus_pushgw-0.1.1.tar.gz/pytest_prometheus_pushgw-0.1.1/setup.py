# setup.py

from setuptools import setup, find_packages

setup(
    name="pytest_prometheus_pushgw",
    version="0.1.1",
    description="Pytest plugin to export test metrics to Prometheus Pushgateway",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="mahsumakbas",
    author_email="mahsum@tigristest.com",
    url="https://github.com/mahsumakbas/pytest_prometheus_pushgw",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pytest>=6.0.0",
        "prometheus_client>=0.14.1"
    ],
    classifiers=[
        "Framework :: Pytest",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.9',
)

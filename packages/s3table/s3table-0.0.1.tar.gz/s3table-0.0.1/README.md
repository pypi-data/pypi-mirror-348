# Getting started with S3Table

S3Table is a Python implementation that leverage PyIceberg for accessing Iceberg tables in AWS S3, without the need of a JVM.

S3Table allows users to create AWS S3 Table with GlueCatalog that can be automatically loaded as external tables into Redshift

## Installation

Before installing S3Table, make sure that you're on an up-to-date version of `pip`:

```sh
pip install --upgrade pip
```

You can install the latest release version from pypi:

```sh
pip install "s3table[s3fs,hive]"
```

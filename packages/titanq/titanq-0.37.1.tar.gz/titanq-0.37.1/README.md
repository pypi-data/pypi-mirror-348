# The TitanQ SDK for Python

![Python](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11-blue) ![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)

TitanQ is the InfinityQ Software Development Kit (SDK) for Python. The SDK facilitates and opens the way for faster implementation
of the TitanQ solver without having to deal directly with the [TitanQ API](https://docs.titanq.infinityq.io).

This TitanQ package is maintained and published by [InfinityQ](https://www.infinityq.tech/)


## API Key

In order to use the TitanQ service, a user needs an API key.
The API key can be obtained by contacting [InfinityQ support](mailto:support@infinityq.tech)


## Installation

The following steps assume that you have:

- A **valid** and **active** API Key
- A supported Python version installed


## Setting up an environment

``` bash
python -m venv .venv
.venv/bin/activate
```


## Install TitanQ

``` bash
pip install titanq
```


## Using TitanQ

The TitanQ solver is designed to support very large problems and therefore very large files. To simplify the user experience, TitanQ will instead use cloud storage set up and managed by the end users.

Currently, the SDK supports two types of storage

| Storage options                | Total input files size         |
|--------------------------------|--------------------------------|
| S3 Buckets                     | ✅ Up to 42GB                  |
| Managed storage                | ⚠️ Up to 1GB                    |

Both options are documented with examples at the TitanQ's [Quickstart documentation](https://docs.titanq.infinityq.io/user-guide/quickstart/sdk-quickstart)

## Problem construction


TitanQ is an optimization solver for highly non-convex optimization problems. Information on problem construction can be found in the [User Guide](https://docs.titanq.infinityq.io/user-guide), and the [SDK Documentation](https://sdk.titanq.infinityq.io/).

Additional parameters are available to tune the problem:
- beta
- coupling_mult
- num_chains
- num_engines

For more informations how to use theses parameters, please refer to the [API documentation](https://docs.titanq.infinityq.io)


## Getting support or help


Further help can be obtained by contacting [InfinityQ support](mailto:support@infinityq.tech)
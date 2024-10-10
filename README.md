# AWS CDK Python Demo: Lambda Function in a Microservice Architecture

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/myarik/aws-cdk-python-demo)

This repository demonstrates how to set up, deploy, and observe an AWS Lambda function in a microservice architecture
using AWS CDK with Python.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Deployment](#deployment)

## Prerequisites

- Python 3.12+
- AWS CLI configured with appropriate permissions
- Node.js and npm (for AWS CDK)
- Poetry for Python dependency management

## Installation

1. Clone the repository:

```bash
git clone https://github.com/myarik/aws-cdk-python-demo.git 
cd aws-cdk-python-demo
```

2. Install the dependencies:

```bash
make dev
```

## Project Structure

```plaintext
aws-cdk-python-demo/
├── app.py                  # CDK app entry point
├── infrastructure/         # CDK stack definitions
├── service/                # Lambda function code
├── tests/                  # Test files
├── Makefile                # Utility commands
├── README.md
└── pyproject.toml          # Python project configuration
```

## Testing

Run tests using:

```bash
make test
```

## Deployment

Deploy the stack:

```bash
make deploy
```

To destroy the stack:

```bash 
make destroy
```

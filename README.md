# AWS CDK Python Demo: Lambda Function in a Microservice Architecture

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/myarik/aws-cdk-python-demo)

This repository demonstrates how to set up, deploy, and observe an AWS Lambda function in a microservice architecture
using AWS CDK with Python.

The repository article can be found [here](https://www.myarik.com/blog/aws_lambda_part1/).

- [Step 1: Setting Up and Structuring the AWS Lambda Project](https://github.com/myarik/aws-cdk-python-demo.git)
- [Step 2: Building and Deploying a Python Lambda Function Using Lambda Layers](https://github.com/myarik/aws_cdk_python_demo/tree/lambda-layers)
- [Step 3: Input Data Validation](https://github.com/myarik/aws_cdk_python_demo/tree/input_validation)
- [Step 4: Setting up Monitoring and Alarms](https://github.com/myarik/aws_cdk_python_demo)

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

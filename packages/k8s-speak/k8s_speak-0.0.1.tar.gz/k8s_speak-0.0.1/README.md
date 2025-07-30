# EKS Speak

A natural language interface for Kubernetes (with Amazon EKS support)

## Overview

EKS Speak is a command-line tool that allows users to interact with Kubernetes clusters using plain English commands. It translates natural language queries into proper `kubectl` commands, making it easier for beginners to work with Kubernetes and for experienced users to speed up common operations.

## Features

- Translate plain English commands to `kubectl` commands
- Support for Amazon EKS clusters
- Context-aware command processing
- Support for common Kubernetes resources:
  - Pods
  - Services
  - Deployments
  - Nodes
  - ConfigMaps
  - Secrets
  - Namespaces
  - Ingresses

## Installation

```bash
# Clone the repository
git clone https://github.com/ImRohitSingh/k8s-speak.git

# Navigate to the project directory
cd k8s-speak

# Install the package
pip install -e .
```

## Prerequisites

- Python 3.6 or higher
- `kubectl` installed and in your PATH
- AWS CLI (for EKS-specific functionality)
- Valid Kubernetes configuration

## Usage

Simply run the `k8s-speak` command to start the interactive shell:

```bash
k8s-speak
```

For verbose output (helpful for debugging):

```bash
k8s-speak -v
```

## Examples

Here are some example commands you can use:

```
k8s-speak> show all pods in namespace kube-system
k8s-speak> get services in production namespace
k8s-speak> list all deployments in namespace default
k8s-speak> describe pod named my-pod-xyz in namespace app
k8s-speak> show nodes in cluster my-eks-cluster
k8s-speak> get logs for pod web-server in namespace frontend
```

## How It Works

1. The tool parses your natural language input
2. It identifies the intent (get, describe, delete, etc.)
3. It extracts resource types, namespaces, and names
4. It constructs the appropriate kubectl command
5. It executes the command and returns the output

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
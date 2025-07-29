# MCP Context SDK

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
![PyPI Version](https://img.shields.io/pypi/v/mcp-context-sdk.svg)
![CI](https://github.com/opencontext-ai/mcp-context-sdk/actions/workflows/ci.yml/badge.svg)

## Overview
The MCP Context SDK is a modular, production-ready Python SDK that enables AI agents, models, and tools to work with structured context schemas. It supports dynamic context construction, prompt generation, and integration with modern AI frameworks.

## Features
- Dynamic context construction and validation
- Schema-to-prompt conversion
- Integration with LangChain, AutoGen, FastAPI, CrewAI, LangGraph, and OpenDevin
- CLI and Streamlit UI demos
- Type hints and schema validations

## Quick Start

### Installation
```bash
pip install mcp-context-sdk
```

### Usage

#### CLI Tool
List available schemas:
```bash
mcp list-schemas coding
```

Convert context to prompt:
```bash
mcp convert-context context.json coding --version v1
```

#### Streamlit UI
Run the Streamlit app to interactively edit and preview context:
```bash
streamlit run examples/streamlit_ui.py
```

## How to Use with LangChain/AutoGen
- Integrate MCP context into LangChain and AutoGen workflows for enhanced AI operations.

## Creating Your Own Schema
- Define domain-specific schemas and integrate them into the MCP SDK.

## Running the Landing Page
To view the landing page locally, open `docs/landing/index.html` in your browser. For deployment, consider using GitHub Pages or Vercel.

## License
This project is licensed under the MIT License.

## Contribution
Contributions are welcome! Please read the [contribution guidelines](docs/contributing.md) first. 
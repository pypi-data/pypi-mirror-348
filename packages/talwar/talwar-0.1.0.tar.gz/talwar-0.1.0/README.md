# TalwarAI 🎯
> A suite of autonomous security agents. Starting with an attack agent, more to come.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Overview
TalwarAI is an AI-powered web application security testing agent that uses Large Language Models (LLMs) to discover and exploit vulnerabilities. This is the first beta release.

## Key Features
- Vulnerability discovery
- Payload generation
- Context-aware testing
- Exploit verification

## Installation

## Setup
1. Install the package:
```bash
pip install -i https://test.pypi.org/simple/ talwarai
```

2. Set up your OpenAI API key:
```bash
# Add this to your ~/.zshrc file
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc

# Source your zsh configuration to apply the changes
source ~/.zshrc
```

You can verify the API key is set by running:
```bash
echo $OPENAI_API_KEY
```

## Basic Usage

```bash
# Basic scan of a intentionally vulnerable site for testing
talwar -t http://testhtml5.vulnweb.com/#/popular
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `-t, --target` | Target URL to test (required) |

## Requirements
- Python 3.9+
- OpenAI API key
- Playwright

## License
MIT License

## Disclaimer
TalwarAI is designed for security professionals and researchers. Use responsibly and ethically. Not intended for malicious purposes.

## 📧 Contact

For questions, feedback, or issues, please reach out to:
- anontech100@gmail.com

---
Made with 🫶🏽 by Anon

# conv2docx

A simple CLI tool to convert JSON/YAML files into Microsoft Word (.docx) documents.

## Overview

This script wraps JSON content in markdown delimiters (```\json```) and uses
 [Pandoc](https://pandoc.org/ ) via the `pypandoc` module to convert it 
 to a `.docx` document — useful when you need to turn structured data into printable
 or editable documents.
 YAML is also supported. It convert to JSON and then processed as JSON/

## Features

- Converts `.json/yaml` files to `.docx`
- Supports single file mode and batch processing
- Automatically creates and cleans up temporary files
- Can be used as a command-line utility

## Usage

To convert a single file:

```bash
conv2docx input.json
```

To convert all .json files in the current directory:

```bash
conv2docx
```

parameter `--keep-temp` keeps temporary files

## Installation

```bash
pip install conv2docx
```

# Requirements

Python >= 3.7


[![License](https://img.shields.io/github/license/AndyTakker/conv2docx)](https://github.com/AndyTakker/conv2docx)


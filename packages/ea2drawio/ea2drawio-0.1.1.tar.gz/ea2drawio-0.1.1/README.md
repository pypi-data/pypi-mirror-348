# ea2drawio

A simple CLI tool to convert diagram from Sparx EA to Drawio file

## Overview

This script wraps JSON content in markdown delimiters (```\json```) and uses
 [Pandoc](https://pandoc.org/ ) via the `pypandoc` module to convert it 
 to a `.docx` document — useful when you need to turn structured data into printable
 or editable documents.

## Features

- Converts `.json` files to `.docx`
- Supports single file mode and batch processing
- Automatically creates and cleans up temporary files
- Can be used as a command-line utility

## Usage

- select diagram in project tree in Sparx EA
- run script ea2drawio
- diagram will be created in current folder

## Installation

```bash
pip install ea2drawio
```

# Requirements

Python >= 3.7

pywin32

[![License](https://img.shields.io/github/license/AndyTakker/ea2drawio)](https://github.com/AndyTakker/ea2drawio)


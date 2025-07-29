# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Rando is a CLI tool that generates random characters based on specified patterns:
- `[x]` for random digits (0-9)
- `[a]` for random lowercase letters (a-z)
- `[A]` for random uppercase letters (A-Z)
- Mixed patterns like `[aA]` for alternating case characters

## Usage

The tool is used with:
```
rando "[FORMAT]"
```

Example: `rando "[xx]-[xxx]-andalso[x]"` might output `42-891-andalso7`

## Testing

Run the tests with:
```
./test_rando.py
```

The test file verifies all supported format patterns and features.

## Implementation Details

The main script (`rando`) processes formats using regex pattern matching to replace bracket expressions with random characters according to the patterns inside the brackets.

Key components:
- Pattern recognition via regex
- Character generation using Python's `random` and `string` modules
- Character-by-character processing for mixed format patterns
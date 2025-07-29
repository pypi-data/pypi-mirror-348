# Rando CLI

A command-line tool for generating random characters based on specified patterns.

## Installation

```bash
pip install rando-cli
```

## Usage

```bash
rando "[FORMAT]"
```

### Format Patterns

- `[x]` - generates a random digit (0-9)
- `[a]` - generates a random lowercase letter (a-z)
- `[A]` - generates a random uppercase letter (A-Z)
- `[aA]` - alternates between lowercase and uppercase

### Examples

```bash
# Generate two random digits
rando "[xx]"
# Output: 42

# Generate complex pattern
rando "[a][x]-[AA]-[xxx]"
# Output: g5-QZ-823

# Mix formats
rando "serial-[aAxAax]"
# Output: serial-rN3Pk7
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/rando-cli.git
cd rando-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Run Tests

```bash
python tests/test_rando.py
```

## License

MIT
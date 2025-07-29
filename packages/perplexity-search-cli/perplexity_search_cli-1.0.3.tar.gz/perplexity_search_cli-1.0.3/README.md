# Perplexity Search CLI

A command line interface for interacting with the Perplexity AI API.

## Features

- Query the Perplexity API from command line
- Accepts input from arguments or stdin
- Supports API key from environment variable or command line
- Optionally save full JSON responses to file
- Clean, formatted output

## Installation

Install directly from PyPI:
```bash
pip install perplexity-search-cli
```

### From source
```bash
git clone https://github.com/yourusername/perplexity-search-cli.git
cd perplexity-search-cli
pip install .
```

### Development install
```bash
git clone https://github.com/yourusername/perplexity-search-cli.git
cd perplexity-search-cli
pip install -e .
```

## Usage

Basic query:
```bash
perplexity-search-cli -p "Your question" -k YOUR_API_KEY
```

Using environment variable:
```bash
export PPLX_API_KEY=YOUR_API_KEY
perplexity-search-cli -p "Your question"
```

Pipe input from stdin:
```bash
echo "Your question" | perplexity-search-cli -k YOUR_API_KEY
```

Save full JSON response:
```bash
perplexity-search-cli -p "Your question" -k YOUR_API_KEY -o response.json
```

## Options

```
  -h, --help            show help message
  -p PROMPT, --prompt PROMPT
                        Prompt to send to Perplexity API
  -k API_KEY, --api-key API_KEY
                        Perplexity API key (or set PPLX_API_KEY env var)
  -o OUTPUT, --output OUTPUT
                        Path to save full JSON response
  --params PARAMS       Additional API parameters as JSON string
```

## Example with Additional Parameters

```bash
perplexity-search-cli -p "Your question" -k YOUR_API_KEY \
  --params '{"temperature": 0.7, "max_tokens": 100}'
```

## Requirements

- Python 3.6+
- requests package

## Publishing New Versions

1. Update version in pyproject.toml
2. Commit changes
3. Create a new git tag:
```bash
git tag vX.Y.Z  # match version in pyproject.toml
git push origin vX.Y.Z
```

The GitHub Action will automatically:
- Build the package
- Publish to PyPI when tags are pushed

# Fast-Password

Fast-Password is a CLI tool and Python library for generating secure, random passwords quickly.

## Installation

Using `pip`

```bash
pip install fast-password
```

Using `uv`

```bash
uv tool install fast-password
```

```bash
uvx --from fast-password fp [OPTIONS] 
```

## CLI Usage

Generate passwords using the `fp` command:

```bash
fp [OPTIONS]
```

### Options

- `-l, --length INT`: Password length (default: 8)
- `-u, --upper`: Include uppercase characters
- `-n, --nums`: Include digits
- `-s, --special`: Include special characters
- `-e, --exclude TEXT`: Exclude specific characters
- `-a, --auto`: Randomly select unspecified options

### Example

```bash
> fp -l 12 -u -n -s
bn6s`c|5*L;8
```

## Library Usage

Use Fast-Password as a library to generate passwords programmatically:

```python
from fast_password import generate

password = generate(length=12, upper=True, nums=True, special=True, exclude="abc")
print(password)
```

## Requirements

- Python >= 3.10
- click >= 8.2.0

## Development

Install dev dependencies:

```bash
uv sync
```

Run tests:

```bash
uv run pytest tests
```

## License

See [LICENSE](LICENSE) file.
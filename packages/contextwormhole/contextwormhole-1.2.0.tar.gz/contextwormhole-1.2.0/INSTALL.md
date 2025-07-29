# Installation Guide for ContextWormhole

## Basic Installation

You can install ContextWormhole directly from PyPI:

```bash
pip install contextwormhole
```

## Development Installation

For development, you can install the package with additional dependencies:

```bash
# Clone the repository
git clone https://github.com/contextwormhole/contextwormhole.git
cd contextwormhole

# Install in development mode with all extras
pip install -e ".[all]"
```

## Optional Dependencies

ContextWormhole provides several optional dependency groups:

- `dev`: Development dependencies (pytest, etc.)
- `docs`: Documentation dependencies (sphinx, etc.)
- `lint`: Linting dependencies (black, flake8, etc.)
- `all`: All optional dependencies

You can install these optional dependencies like this:

```bash
# Install with development dependencies
pip install contextwormhole[dev]

# Install with documentation dependencies
pip install contextwormhole[docs]

# Install with linting dependencies
pip install contextwormhole[lint]

# Install with all optional dependencies
pip install contextwormhole[all]
```

## Requirements

ContextWormhole requires:

- Python 3.8 or later
- PyTorch 1.9.0 or later
- Transformers 4.20.0 or later
- NumPy 1.20.0 or later (but less than 2.0.0 for PyTorch compatibility)

## GPU Support

For optimal performance with large models, a CUDA-compatible GPU is recommended. ContextWormhole will automatically use CUDA if available.

## Troubleshooting

If you encounter any issues during installation, please check:

1. That you have the correct Python version (3.8+)
2. That you have compatible versions of PyTorch and Transformers
3. For GPU usage, that you have the correct CUDA version installed

For more help, please open an issue on our [GitHub repository](https://github.com/contextwormhole/contextwormhole/issues).
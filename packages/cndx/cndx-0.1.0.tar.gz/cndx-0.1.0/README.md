# cndx

Minimal CLI wrapper for `conda project run`. Installable via PyPI. Inspired by tools like `uvx`.

## Install

```bash
pip install cndx
```

## Usage

```bash
cndx python script.py
```

This is equivalent to:

```bash
conda project run python script.py
```

All arguments after `cndx` are passed through.
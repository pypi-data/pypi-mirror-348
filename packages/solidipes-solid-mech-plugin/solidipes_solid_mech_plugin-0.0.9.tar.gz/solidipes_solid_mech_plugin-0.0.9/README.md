# Solidipes solid mechanics plugin

_Plugin for Solidipes with solid mechanics components_

[![PyPI version](https://badge.fury.io/py/solidipes-solid-mech-plugin.svg)](https://badge.fury.io/py/solidipes-solid-mech-plugin)

Meant to be used with [Solidipes](https://gitlab.com/solidipes/solidipes).


## Dependencies

```bash
sudo apt install libgl1-mesa-glx xvfb
```


# Installation for development

```bash
git clone https://gitlab.com/solidipes/solidipes-solid-mech-plugin.git
cd solidipes-solid-mech-plugin
pip install -e .[dev]
pre-commit install
```


# Running tests

```bash
pytest
```

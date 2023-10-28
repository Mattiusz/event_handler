# event_handler
This a simple fast api server used to provide a REST API for events and attendees.


## Requirements

Python >= 3.11


## Installation

```bash
cd event_handler

# Create a virtual environemt.
python3.11 -m venv venv
source venv/bin/activate

# Install package as editable including development requirements.
make install-dev
```

## Start
```bash
make run
```
or:
```bash
python3.11 event_handler/main.py
```

This starts a fastapi webserver at http://127.0.0.1:8000/docs if the enviroment is configured to start locally.


## Development

Common task are available using the `make`.
Here is a list of available commands:

```bash
clean                Remove all Python artifacts.
clean-pyc            Remove Python file artifacts.
clean-dist           Clean build artifacts.
test                 Run tests quickly with the default Python.
coverage             Run coverage.
format               Format code following configured styleguide.
install-dev          Install all dependencies needed for development to the active Python site-packages.
install-pkg          Install the package to the active Python site-packages.
bumbversion          Bump version based on conventional commits.
dump-requirements    Dumps current pip dependencies into a requirements.txt
changelog            Generate CHANGELOG.md based on conventional commits.
check-version        Check versions of installed packages.
run                  Runs application
```

This repository makes use of [pre-commit hooks](https://pre-commit.com)
to automatically do some cleanup and enforce code style before something is
actually commited.

# pytest-iso

`pytest-iso` is a `pytest` plugin written in Rust that automatically generates PDF test reports. Designed for code audit documentation or general test reporting.


## Contents

- [Features](#features)
- [Use Cases](#use-cases)
- [Installation](#installation)
- [Usage](#usage)
- [Known Issues](#known-issues)
- [License](#license)
- [Contributing](#contributing)

## Features

- Automatically generates a PDF report (`test_protocol.pdf`) from pytest results
- Rust-powered performance
- Seamless integration with `pytest`
- Well suited for creating audit‑ready or compliance documentation

This project is under active development. Expect breaking changes and incomplete features. See [Known Issues](#known-issues)
for further information.

## Use cases

Many projects require verifiable, human-readable test documentation. `pytest-iso` bridges automated testing with audit-ready PDF reports, making it ideal for:

- ISO 27001 or ISO 9001 software audits
- Certification processes
- Offline archiving of test evidence

**Disclaimer:** `pytest-iso` is not officially certified or endorsed by the International Organization for Standardization (ISO). 
Please confirm that its reports meet your specific compliance requirements before use.

## Installation

Pytest-iso supports Python >= 3.9. `Pytest` will automatically detect the plugin via the pytest-entrypoint provided by `pytest-iso`.

```bash
pip install pytest-iso
```

## Usage

Pytest-iso will automatically execute after execution of pytest. 

```bash
pytest tests
```

As a result a PDF file (`test_protocol.pdf`) will be produced in the root directory.

```bash
==================== test session starts ==================
platform win32 -- Python 3.13.0, pytest-8.3.5, pluggy-1.5.0
rootdir: ./pytest-iso
configfile: pyproject.toml
plugins: anyio-4.7.0, cov-6.1.1, iso-0.3.0, xdist-3.6.1
collected 4 items

tests/test_plugin.py ....
Generated PDF report: test_protocol.pdf
```

As part of a CI stage, the resulting `test_protocol.pdf` can be pushed to the artifacts:

```bash
#.gitlab-ci.yml
test_py:
  stage: test_py
  image: python:3.13
  before_script:
    - pip install pytest pytest-iso
  script:
    - pytest -s tests
  artifacts:
    paths:
      - test_protocol.pdf
```

An example PDF file can be found under `examples/test_protocol.pdf`.

## Known issues

- PDF layout is still minimal and not "audit-ready" (e.g., needs signature field)
- Layout is currently not customizable (e.g., which sections to print or option to add a company logo)
- Currently, pre-built wheels are only provided for Linux platforms

## License

This library is MIT-licensed. 

Included font files (Roboto) are licensed under the SIL Open Font License 1.1. See pytest_iso/fonts/OFL.txt for details.

## Contributing

Contributions are always welcome! Please see [`CONTRIBUTING.md`](https://gitlab.com/sdirndorfer_pr/pytest-iso/-/blob/main/CONTRIBUTING.md?ref_type=heads).
# rust-code-analysis-python

Python bindings for [rust-code-analysis](https://github.com/mozilla/rust-code-analysis), a Rust library to analyze and collect metrics on source code.

## Installation

```bash
pip install rust-code-analysis-python
```

## Usage

```python
from rust_code_analysis_python import compute_metrics, remove_comments

# Get code metrics
metrics_result = compute_metrics("example.rs", code_string, unit=True)

# Remove comments from code
code_without_comments = remove_comments("example.rs", code_string)
```

Consult docstrings for details.

## Developing

```bash
# Install rust and pip install build tox
python -m build
# Run tests
tox run
```

## License

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/. 
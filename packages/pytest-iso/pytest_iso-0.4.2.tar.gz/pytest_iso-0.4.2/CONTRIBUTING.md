# How to contribute to pytest-iso

This file is in an early stage and will be extended in the future.


## General structure of the codebase

It's a mixed Python/Rust package, that exposes Rust functionalities to Python via PyO3. However, since it is
a pytest-plugin there are also some pure Python functionalities necessary, like pytest hooks.

The project was initialized using `maturin new`. See [maturin readme](https://github.com/PyO3/maturin).

To enable the pytest/pytest-iso communication an [entrypoint for pytest](https://doc.pytest.org/en/latest/how-to/writing_plugins.html#making-your-plugin-installable-by-others) is necessary.

## Pre-Commit

[Pre-Commit](https://pre-commit.com/) is used to locally run linters and formatters for Python and Rust.

Activate pre-commit as follows:

```bash
cd pytest-iso
pip install pre-commit
pre-commit install
```

## Versioning

The tool [bumpver](https://pypi.org/project/bumpver/) is used to increment version numbers:

- Create a new branch
- Run `bumpver --update --major/--minor/--patch --allow-dirty`
- Push and create an MR `git push -o merge_request.create -o merge_request.squash`
- Recreate Cargo.Lock by running `cargo generate-lockfile`
- Move changes described in the Unreleased section of the Changelog under the new version number
- Commit and push to the created MR
- After merging the MR checkout main and pull latests changes
- Create a tag on the main branch: `git tag $VERSION` (align Version with the version set by bumpver)
- `git push tags`
# Lib-version

`lib-version` is a version-aware Python library. It keeps track of its own version when requested.

## 📚 Table of Contents

- [Installation and Development](#-installationanddevelopment)
- [🛠 Requirements](#-requirements)
- [⚙️ Release Workflow](#️-releaseworkflow)

## [Installation and Development](#-installationanddevelopment)

To install the library, use the following command:

```bash
pip install .
```
To set up a development environment, install the optional build tools:

```bash
pip install -r requirements.txt
```

## [🛠 Requirements](#-requirements)

The library requires Python 3.10.

## [⚙️ Release Workflow](#️-releaseworkflow)
The project uses GitHub Actions to automate the release process. When a new tag is pushed in the format `v<MAJOR>.<MINOR>.<PATCH>`, the workflow will:

1. Parse the version from the tag.
2. Inject the version into `pyproject.toml`.
3. Build the package.
4. Publish the package to PyPI registry

## Contact

For any questions or issues, please contact the maintainers of the repository.
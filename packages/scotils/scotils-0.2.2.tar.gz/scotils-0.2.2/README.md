Scotils Monorepo
A collection of Python utilities under the scotils namespace, managed as a uv workspace.
Packages

scotils-finance: Financial utilities (pip install scotils-finance)
scotils-strings: String manipulation utilities (pip install scotils-strings)
scotils: Metapackage for installing all utilities (pip install scotils[all])

Installation
Install individual packages:
pip install scotils-finance
pip install scotils-strings

Install all packages:
pip install scotils[all]

Development

Uses uv for dependency management and workspace support.
Uses setuptools for building and packaging.
Managed as a uv workspace with a single uv.lock for consistent dependencies.

Setup
uv sync --all-packages

Lock Dependencies
uv lock

Build
cd packages/scotils-finance
uv build

Publish
uv publish

Repository
Hosted on GitLab: https://gitlab.com/your-org/scotils
License
MIT

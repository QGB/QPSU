# PyPI Trusted Publishing

To enable trusted publishing for this project, configure a pending publisher on PyPI with:

- Project name: qpsu
- Owner: qgb
- Repository: qpsu
- Workflow name: publish-to-pypi.yml
- Environment: pypi

This repository already contains a GitHub Actions workflow at .github/workflows/publish-to-pypi.yml that uses the PyPI trusted publishing action.

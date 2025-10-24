# Contribution

Thank you for your interest in contributing to the `pyprintf` Python library! We value contributions from the community to enhance this project for all users. Whether you're fixing bugs, adding features, improving documentation, or extending functionality, your efforts are greatly appreciated.

---

## Code of Conduct

By participating in this project, you agree to adhere to our [Code of Conduct](https://github.com/playfulsparkle/.github/blob/main/CODE_OF_CONDUCT.md). Please review it before engaging with the community.

---

## Getting Started

### Prerequisites

To contribute effectively, ensure you have:

- A basic understanding of Git and GitHub workflows
- Familiarity with Python development
- Python 3.10 or higher installed on your system
- A virtual environment for testing and development
- `pip` and `setuptools` installed
- Access to the project's dependencies (see `pyproject.toml`)

---

## How to Contribute

### Reporting Issues

To report an issue:

1. Review the [existing issues](https://github.com/playfulsparkle/pyprintf/issues) to avoid duplicates, or open a ticket on the [support page](https://support.playfulsparkle.com/).
2. Provide detailed information, including:
   - Python version
   - Steps to reproduce the issue
   - Expected and actual behavior
   - Screenshots or logs (if applicable)
   - Any relevant error messages or stack traces

### Suggesting Features

To propose a new feature, open an issue and include:

- The problem your feature addresses
- A clear and concise description of the proposed solution
- Relevant use cases or examples

### Submitting Pull Requests

To submit a pull request (PR):

1. Fork the repository.
2. Create a descriptive branch:
   `git checkout -b feat/your-feature-name` or `fix/your-bug-name`
3. Install the project in editable mode:
   ```bash
   pip install -e .
   ```
4. Commit your changes with meaningful messages.
5. Push your branch:
   `git push origin your-branch-name`
6. Open a PR with a clear title and detailed description.

---

## Pull Request Process

1. Ensure your changes are compatible with supported Python environments (Python 3.10+).
2. Update relevant documentation (e.g., README, inline comments) as needed.
3. Submit your PR for review. Maintainers may request changes.
4. Once approved, your contribution will be merged into the project.

---

## Style Guidelines

### Code Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding standards.
- Use descriptive and meaningful names for variables and functions.
- Add comments to clarify complex logic.

### Commit Messages

- Write in present tense (e.g., "Add feature" instead of "Added feature").
- Limit the first line to 72 characters.
- Provide additional details in the body if necessary.

---

## Testing Guidelines

To ensure the quality of your contributions:

- Test changes in a virtual environment.
- Validate edge cases, such as different input formats or special characters.
- Confirm that your changes do not conflict with existing functionality.
- Use the `Makefile` commands for testing and linting:
  - `make test` to run tests
  - `make lint` to check for linting issues
  - `make coverage` to generate a test coverage report

---

## License Agreement

By contributing to this project, you agree that your work will be licensed under the project's [BSD-3-Clause License](LICENSE).

---

## Contributor Recognition

We value and acknowledge significant contributions. Contributors may be recognized in:

- The project's README
- Release notes
- A dedicated "Contributors" section

---

## Questions or Support?

If you have any questions or need assistance, feel free to reach out via:

- [GitHub Issues](https://github.com/playfulsparkle/pyprintf/issues)
- [support@playfulsparkle.com](mailto:support@playfulsparkle.com)

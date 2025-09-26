# Contributing to REB-1

Thanks for considering contributing!

## Development workflow

1. **Fork** this repository and clone your fork in WSL2 or Linux.
2. Create a virtual environment with Python 3.10.
   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
3. Run style checks and tests:
   ruff check .
   black --check .
   pytest
4. Make your changes in a feature branch.
5. Submit a pull request with a clear description of what you added or fixed.

## Guidelines
- Follow PEP8 style (enforced by ruff + black).
- Keep dependencies minimal.
- Ensure CI passes before requesting review.
- Add/update unit tests when changing functionality.
- Update the CHANGELOG.md for user-facing changes.

## Communication
- File issues for bugs or feature requests.

By contributing, you agree to abide by our Code of Conduct.
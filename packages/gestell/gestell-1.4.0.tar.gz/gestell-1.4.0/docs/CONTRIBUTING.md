# 3 Contributing

All workflows in the SDK use [ruff](https://github.com/astral-sh/ruff) and [uv](https://github.com/astral-sh/uv).

## Guidelines

Opening an issue to address your concern is recommended. However, if you plan to submit a pull request (PR), please adhere to the following:

 1. **Align with the Repo Structure**: Organize canonical functionality within the appropriate folders. Provide clear documentation and usage annotations in the base class structures.

 2. **Pass All Unit Tests**: Ensure all `pytest` unit tests pass and maintain near full code coverage.

 3. **Provide a Detailed PR Description**: Clearly outline the changes made and the specific issues they resolve in your pull request.

## Workflow

```bash
# Run unit tests
ruff check
ruff format
uv run pytest
uv run coveralls

# Compile a new dist
uv venv
rm -rf dist
uv build

# Verify and test the package externally with uv and a normal venv environment
cd ..
uv init test
cd test
uv add ../python-sdk
uv pip install ../python-sdk/dist/gestell-1.4.0-py3-none-any.whl
```

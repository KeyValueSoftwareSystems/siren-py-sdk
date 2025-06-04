# Siren AI Python SDK (`siren-ai`)

This is the official Python SDK for the Siren notification platform.

## Installation

```bash
pip install siren-ai
```

## Basic Usage

```python
from siren import SirenClient

client = SirenClient(api_key="YOUR_API_KEY")

# Example: Send a message
response = client.send_message({
    "to": "user@example.com",
    "template": "ai_task_completed",
    "data": {
        "task_name": "Data Cleanup",
        "result": "Success"
    }
})

print(response)
```

## Getting Started for Package Developers

This guide will help you set up your environment to contribute to the `siren-ai` SDK.

### Prerequisites

*   Git
*   Python 3.8 or higher
*   `uv` (installed, see [uv installation guide](https://github.com/astral-sh/uv#installation))

### Setup Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/siren-ai.git # TODO: Update with actual repo URL
    cd siren-ai
    ```

2.  **Create a virtual environment using `uv`:**
    This creates an isolated environment in a `.venv` directory.
    ```bash
    uv venv
    ```

3.  **Activate the virtual environment:**
    Commands will now use this environment's Python and packages.
    ```bash
    source .venv/bin/activate
    ```
    *(On Windows, use: `.venv\Scripts\activate`)*

4.  **Install dependencies with `uv`:**
    This installs `siren-ai` in editable mode (`-e`) and all development dependencies (`.[dev]`).
    ```bash
    uv pip install -e ".[dev]"
    ```

5.  **Set up pre-commit hooks:**
    (Ensures code quality before commits. Run from the activated environment or use `uv run ...`)
    ```bash
    pre-commit install
    ```
    You can also run all hooks manually:
    ```bash
    pre-commit run --all-files
    ```

6.  **Run tests:**
    (Verify the setup and SDK functionality. Run from the activated environment or use `uv run ...`)
    ```bash
    pytest
    ```

7.  **Start developing!**
    You are now ready to contribute to the `siren-ai` SDK.

### Code Style & Linting

*   Code style is enforced by `ruff` (linting, formatting, import sorting) and `pyright` (type checking).
*   These tools are automatically run via pre-commit hooks.

### Submitting Changes

*   Create a feature branch for your changes.
*   Commit your changes (pre-commit hooks will run).
*   Push your branch and open a Pull Request against the main repository branch.

## Contributing

Contribution guidelines will be added here.

## License

This project will be licensed under the [Specify License, e.g., MIT License].

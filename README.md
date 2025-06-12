# Siren Python SDK

This is the official Python SDK for the [Siren notification platform](https://docs.trysiren.io).

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [SDK Methods](#sdk-methods)
- [Examples](#examples)
- [For Package Developers](#getting-started-for-package-developers)
- [Future Enhancements](#future-enhancements)

## Installation

```bash
pip install siren-ai
```

## Basic Usage

```python
from siren import SirenClient

# Initialize the client
client = SirenClient(api_key="YOUR_SIREN_API_KEY")

# Send a message
message_id = client.message.send(
    template_name="welcome_email",
    channel="EMAIL",
    recipient_type="direct",
    recipient_value="user@example.com",
    template_variables={"user_name": "John Doe"}
)
print(f"Message sent! ID: {message_id}")

# To specify env
client = SirenClient(api_key="YOUR_SIREN_API_KEY", env="dev")
```

## SDK Methods

The Siren-AI Python SDK provides a clean, namespaced interface to interact with the Siren API.

**Templates** (`client.template.*`)
- **`client.template.get()`** - Retrieves a list of notification templates with optional filtering, sorting, and pagination
- **`client.template.create()`** - Creates a new notification template
- **`client.template.update()`** - Updates an existing notification template
- **`client.template.delete()`** - Deletes an existing notification template
- **`client.template.publish()`** - Publishes a template, making its latest draft version live

**Channel Templates** (`client.channel_template.*`)
- **`client.channel_template.create()`** - Creates or updates channel-specific templates (EMAIL, SMS, etc.)
- **`client.channel_template.get()`** - Retrieves channel templates for a specific template version

**Messaging** (`client.message.*`)
- **`client.message.send()`** - Sends a message using a template to a recipient via a chosen channel
- **`client.message.get_replies()`** - Retrieves replies for a specific message ID
- **`client.message.get_status()`** - Retrieves the status of a specific message (SENT, DELIVERED, FAILED, etc.)

**Workflows** (`client.workflow.*`)
- **`client.workflow.trigger()`** - Triggers a workflow with given data and notification payloads
- **`client.workflow.trigger_bulk()`** - Triggers a workflow in bulk for multiple recipients
- **`client.workflow.schedule()`** - Schedules a workflow to run at a future time (once or recurring)

**Webhooks** (`client.webhook.*`)
- **`client.webhook.configure_notifications()`** - Configures webhook URL for receiving status updates
- **`client.webhook.configure_inbound()`** - Configures webhook URL for receiving inbound messages

**Users** (`client.user.*`)
- **`client.user.add()`** - Creates a new user or updates existing user with given unique_id
- **`client.user.update()`** - Updates an existing user's information
- **`client.user.delete()`** - Deletes an existing user

## Examples

For detailed usage examples of all SDK methods, see the [examples](./examples/) folder.

## For Package Developers

### Environment Configuration

For testing the SDK, set these environment variables:

- **`SIREN_API_KEY`**: Your API key from the Siren dashboard
- **`SIREN_ENV`**: Set to `dev` for development/testing (defaults to `prod`)

### Prerequisites

*   Git
*   Python 3.8 or higher
*   `uv` (installed, see [uv installation guide](https://github.com/astral-sh/uv#installation))

### Setup Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jithu-keyvalue/siren-ai.git
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
    (Ensures code quality before commits)
    ```bash
    uv run pre-commit install
    ```

    You are now ready to contribute to the `siren-ai` SDK!
    Try `$ python examples/webhooks.py`

### Code Style & Linting

*   Code style is enforced by `ruff` (linting, formatting, import sorting) and `pyright` (type checking).
*   These tools are automatically run via pre-commit hooks.

### Running Tests

To run the test suite, use the following command from the project root directory:

```bash
uv run pytest
```

This will execute all tests defined in the `tests/` directory.

### Submitting Changes

*   Create a feature branch for your changes.
*   Commit your changes (pre-commit hooks will run).
*   Push your branch and open a Pull Request against the `develop` repository branch.

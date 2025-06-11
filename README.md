# Siren AI Python SDK (`siren-ai`)

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
message_id = client.send_message(
    template_name="welcome_email",
    channel="EMAIL",
    recipient_type="direct",
    recipient_value="user@example.com",
    template_variables={"user_name": "John Doe"}
)
print(f"Message sent! ID: {message_id}")
```

## SDK Methods

The Siren-AI Python SDK provides an interface to interact with the Siren API.

**Templates**
- **`get_templates()`** - Retrieves a list of notification templates with optional filtering, sorting, and pagination
- **`create_template()`** - Creates a new notification template
- **`update_template()`** - Updates an existing notification template
- **`delete_template()`** - Deletes an existing notification template
- **`publish_template()`** - Publishes a template, making its latest draft version live
- **`create_channel_templates()`** - Creates or updates channel-specific templates (EMAIL, SMS, etc.)
- **`get_channel_templates()`** - Retrieves channel templates for a specific template version

**Messaging**
- **`send_message()`** - Sends a message using a template to a recipient via a chosen channel
- **`get_replies()`** - Retrieves replies for a specific message ID
- **`get_message_status()`** - Retrieves the status of a specific message (SENT, DELIVERED, FAILED, etc.)

**Workflows**
- **`trigger_workflow()`** - Triggers a workflow with given data and notification payloads
- **`trigger_bulk_workflow()`** - Triggers a workflow in bulk for multiple recipients
- **`schedule_workflow()`** - Schedules a workflow to run at a future time (once or recurring)

**Webhooks**
- **`configure_notifications_webhook()`** - Configures webhook URL for receiving status updates
- **`configure_inbound_message_webhook()`** - Configures webhook URL for receiving inbound messages

**Users**
- **`add_user()`** - Creates a new user or updates existing user with given unique_id
- **`update_user()`** - Updates an existing user's information
- **`delete_user()`** - Deletes an existing user

## Examples

For detailed usage examples of all SDK methods, see the [examples](./examples/) folder.

## For Package Developers

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

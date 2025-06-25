# Siren Python SDK

This is the official Python SDK for the [Siren notification platform](https://docs.trysiren.io).

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [SDK Methods](#sdk-methods)
- [Examples](#examples)
- [For Package Developers](#for-package-developers)

## Installation

```bash
pip install siren-ai
```

## Basic Usage

### Synchronous
```python
from siren import SirenClient


# Uses SIREN_API_KEY and SIREN_ENV environment variables
client = SirenClient()

# Send a direct message without template
message_id = client.message.send(
    recipient_value="alice@company.com",
    channel="EMAIL",
    body="Your account has been successfully verified. You can now access all features."
)

# Send a message using a template
message_id = client.message.send(
    recipient_value="U01UBCD06BB",
    channel="SLACK",
    template_name="welcome_template",
    template_variables={"user_name": "John"},
)

# Send a message with specific provider
from siren.models.messaging import ProviderCode
message_id = client.message.send(
    recipient_value="alice@company.com",
    channel="EMAIL",
    body="Your account has been successfully verified.",
    provider_name="email-provider",
    provider_code=ProviderCode.EMAIL_SENDGRID,
)

# Send a message using awesome template
message_id = client.message.send_awesome_template(
    recipient_value="U01UBCD06BB",
    channel="SLACK",
    template_identifier="awesome-templates/customer-support/escalation_required/official/casual.yaml",
    template_variables={
        "ticket_id": "123456",
        "customer_name": "John",
        "issue_summary": "Payment processing issue",
        "ticket_url": "https://support.company.com/ticket/123456",
        "sender_name": "Support Team"
    },
    provider_name="slack-provider",
    provider_code=ProviderCode.SLACK,
)
```

```python
# You can also do:
client = SirenClient(api_key="YOUR_SIREN_API_KEY") # default env is "prod"

# Or:
client = SirenClient(api_key="YOUR_SIREN_API_KEY", env="dev")
```

### Asynchronous
```python
from siren import AsyncSirenClient

# Using async context manager (recommended)
async with AsyncSirenClient() as client:
    message_id = await client.message.send(
        recipient_value="alice@company.com",
        channel="EMAIL",
        body="Your account has been successfully verified. You can now access all features."
    )

# Or manually managing the client
client = AsyncSirenClient()
try:
    message_id = await client.message.send(
        recipient_value="alice@company.com",
        channel="EMAIL",
        body="Your account has been successfully verified. You can now access all features."
    )
finally:
    await client.aclose()
```

All synchronous methods have a 1-to-1 asynchronous equivalent—just `await` them on the async client.

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
- **`client.message.send()`** - Sends a message (with or without a template) to a recipient via a chosen channel
- **`client.message.send_awesome_template()`** - Sends a message using a template path/identifier
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

     Try `$ python examples/messaging_async.py`

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


## Changes planned
- Check how critical is .close() for async client, explore ways to avoid that.

# Siren AI Python SDK (`siren-ai`)

This is the official Python SDK for the [Siren notification platform](https://docs.trysiren.io).

## Table of Contents

- [Siren AI Python SDK (`siren-ai`)](#siren-ai-python-sdk-siren-ai)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
  - [Features](#features)
    - [`get_templates()`](#get_templates)
    - [`create_template()`](#create_template)
    - [`update_template()`](#update_template)
    - [`delete_template()`](#delete_template)
    - [`publish_template()`](#publish_template)
    - [`create_channel_templates()`](#create_channel_templates)
    - [`get_channel_templates()`](#get_channel_templates)
    - [`trigger_workflow()`](#trigger_workflow)
    - [`trigger_bulk_workflow()`](#trigger_bulk_workflow)
  - [Getting Started for Package Developers](#getting-started-for-package-developers)
    - [Prerequisites](#prerequisites)
    - [Setup Steps](#setup-steps)
    - [Code Style \& Linting](#code-style--linting)
    - [Running Tests](#running-tests)
    - [Submitting Changes](#submitting-changes)
  - [Future Enhancements](#future-enhancements)

## Installation

```bash
pip install siren-ai
```

## Basic Usage

```python
from siren import SirenClient

# Initialize the client by passing your API key:
client = SirenClient(api_key="YOUR_SIREN_API_KEY")

# Example: Get templates
# Get the first 5 templates
templates_response = client.get_templates(page=0, size=5)
print(templates_response)
```

## Features

The Siren-AI Python SDK provides an interface to interact with the Siren API.

### `get_templates()`

Retrieves a list of notification templates.

**Parameters:**
*   Supports optional filtering (`tag_names`, `search`), sorting (`sort`), and pagination (`page`, `size`). Refer to the official Siren API documentation for detailed parameter usage.

**Example:**
```python
# Get 5 templates, sorted by name
templates_response = client.get_templates(size=5, sort="name,asc")
print(templates_response)
```

### `create_template()`

Creates a new notification template.

**Parameters:**
*   `template_data` (Dict[str, Any]): A dictionary representing the template structure. Key fields include `name`, `configurations`, etc. For the detailed payload structure, please refer to the official Siren API documentation.

**Example:**
```python
new_template_payload = {
  "name": "SDK_Quick_Template",
  "configurations": {
    "EMAIL": {
      "subject": "Quick Test",
      "body": "<p>Hello via SDK!</p>"
    }
  }
}
created_template_response = client.create_template(new_template_payload)
print(created_template_response)
```

### `update_template()`

Updates an existing notification template.

**Parameters:**
*   `template_id` (str): The ID of the template to update.
*   `template_data` (Dict[str, Any]): A dictionary containing the template fields to update. For the detailed payload structure, please refer to the official Siren API documentation.

**Example:**
```python
existing_template_id = "YOUR_EXISTING_TEMPLATE_ID"
update_payload = {
  "name": "Updated SDK Template Name",
  "description": "This template was updated via the SDK.",
  "tagNames": ["sdk-updated"]
}

updated_template_response = client.update_template(existing_template_id, update_payload)
print(updated_template_response)

```

### `delete_template()`

Deletes an existing notification template.

**Parameters:**
*   `template_id` (str): The ID of the template to delete.

**Example:**
```python
template_id_to_delete = "YOUR_TEMPLATE_ID_TO_DELETE"

delete_response = client.delete_template(template_id_to_delete)
print(delete_response)

```

### `publish_template()`

Publishes an existing notification template, making its latest draft version live.

**Parameters:**
*   `template_id` (str): The ID of the template to publish.

**Example:**
```python
template_id_to_publish = "YOUR_TEMPLATE_ID_TO_PUBLISH"

publish_response = client.publish_template(template_id_to_publish)
print(publish_response)
```

### `create_channel_templates()`

Creates or updates channel-specific templates for a given template ID. This method allows you to define different content and settings for various notification channels (e.g., EMAIL, SMS) associated with a single parent template.

**Parameters:**
*   `template_id` (str): The ID of the template for which to create/update channel templates.
*   `channel_templates` (Dict[str, Any]): A dictionary where keys are channel names (e.g., "EMAIL", "SMS") and values are the channel-specific template objects. Each object should conform to the structure expected by the Siren API for that channel.

**Example:**
```python
template_id = "YOUR_TEMPLATE_ID"
channel_templates_payload = {
    "SMS": {
        "body": "New SMS content via SDK for {{variable_name}}",
        "channel": "SMS",
        "isFlash": False
    },
    "EMAIL": {
        "subject": "Channel Config Update for {{variable_name}}",
        "body": "<p>Updated email body for channel config.</p>",
        "channel": "EMAIL"
    }
}

response = client.create_channel_templates(template_id, channel_templates_payload)
print(response)
```

### `get_channel_templates()`

Retrieves the channel templates associated with a specific template version ID.

**Parameters:**
*   `version_id` (str): The ID of the template version for which to fetch channel templates.
*   Optional query parameters:
    *   `channel` (str): Filter by a specific channel (e.g., "EMAIL", "SMS").
    *   `search` (str): Search term to filter channel templates.
    *   `sort` (str): Sort order (e.g., "channel,asc").
    *   `page` (int): Page number for pagination.
    *   `size` (int): Number of items per page.

**Example:**
```python
# Replace with an actual template version ID
template_version_id = "YOUR_TEMPLATE_VERSION_ID"

# Get all channel templates for a version
channel_templates_response = client.get_channel_templates(version_id=template_version_id)
print(channel_templates_response)

# Get SMS channel templates for a version, first page, 5 items
sms_channel_templates = client.get_channel_templates(
    version_id=template_version_id,
    channel="SMS",
    page=0,
    size=5
)
print(sms_channel_templates)
```

### `trigger_workflow()`

Triggers a specified workflow with the given data and notification payloads.

**Parameters:**
*   `workflow_name` (str): The name of the workflow to be executed.
*   `data` (Optional[Dict[str, Any]]): Common data that will be used across all workflow executions. Defaults to `None`.
*   `notify` (Optional[Dict[str, Any]]): Specific data for this particular workflow execution. Defaults to `None`.

**Example:**
```python
workflow_to_trigger = "otp_workflow"
data_payload = {
  "subject": "Your One-Time Password",
  "user_id": "user_12345"
}
notify_payload = {
  "notificationType": "email",
  "recipient": "customer@example.com",
  "name": "John Doe"
}

trigger_response = client.trigger_workflow(
    workflow_name=workflow_to_trigger,
    data=data_payload,
    notify=notify_payload
)
print(trigger_response)

# Example: Triggering a workflow with only the name
minimal_trigger_response = client.trigger_workflow(workflow_name="simple_workflow")
print(minimal_trigger_response)
```

### `trigger_bulk_workflow()`

Triggers a specified workflow in bulk for multiple recipients/notifications, with common data applied to all and specific data for each notification.

**Parameters:**
*   `workflow_name` (str): The name of the workflow to be executed.
*   `notify` (List[Dict[str, Any]]): A list of notification objects. Your workflow will be executed for each object in this list. Each object contains specific data for that particular workflow execution.
*   `data` (Optional[Dict[str, Any]]): Common data that will be used across all workflow executions. Defaults to `None`.

**Example:**
```python
workflow_to_trigger_bulk = "onboarding_sequence"
common_payload = {
  "campaign_source": "webinar_signup_2024"
}
individual_notifications = [
    {
      "notificationType": "email",
      "recipient": "user_a@example.com",
      "name": "Alex",
      "join_date": "2024-06-01"
    },
    {
      "notificationType": "sms",
      "recipient": "+15550001111",
      "segment": "trial_user"
    },
    {
      "notificationType": "email",
      "recipient": "user_b@example.com",
      "name": "Beth",
      "join_date": "2024-06-02"
    }
]

bulk_response = client.trigger_bulk_workflow(
    workflow_name=workflow_to_trigger_bulk,
    notify=individual_notifications,
    data=common_payload
)
print(bulk_response)

# Example: Bulk triggering with only notify list (no common data)
minimal_bulk_response = client.trigger_bulk_workflow(
    workflow_name="simple_bulk_actions",
    notify=[
        {"action": "activate_feature_x", "user_id": "user_c@example.com"},
        {"action": "send_survey_y", "user_id": "user_d@example.com"}
    ]
)
print(minimal_bulk_response)
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
*   Push your branch and open a Pull Request against the main repository branch.

## Future Enhancements

- Expand SDK for full Siren API endpoint coverage.
- Implement typed response models (e.g., Pydantic) for robust data handling.
- Introduce custom SDK exceptions for improved error diagnostics.

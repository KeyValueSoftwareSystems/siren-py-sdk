# Siren AI Python SDK (`siren-ai`)

This is the official Python SDK for the Siren notification platform.

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Features](#features)
  - [`get_templates()`](#get_templates)
  - [`create_template()`](#create_template)
  - [`update_template()`](#update_template)
  - [`delete_template()`](#delete_template)
  - [`publish_template()`](#publish_template)
  - [`create_channel_configurations()`](#create_channel_configurations)
- [Getting Started for Package Developers](#getting-started-for-package-developers)

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

### `create_channel_configurations()`

Creates or updates the channel-specific configurations (e.g., for EMAIL, SMS) for a given template.

**Parameters:**
*   `template_id` (str): The ID of the template for which to create/update channel configurations.
*   `configurations` (Dict[str, Any]): A dictionary where keys are channel types (e.g., "EMAIL", "SMS") and values are the respective configuration objects. For the detailed payload structure for each channel, please refer to the official Siren API documentation.

**Example:**
```python
template_id = "YOUR_TEMPLATE_ID"
channel_configs_payload = {
    "SMS": {
        "body": "New SMS content via SDK for {{variable_name}}",
        "channel": "SMS", # Ensure channel is specified within its config
        "isFlash": False
    },
    "EMAIL": {
        "subject": "Channel Config Update for {{variable_name}}",
        "body": "<p>Updated email body for channel config.</p>",
        "channel": "EMAIL" # Ensure channel is specified
    }
}

response = client.create_channel_configurations(template_id, channel_configs_payload)
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
    You can also run all hooks manually:
    ```bash
    uv run pre-commit run --all-files
    ```

6.  **Run tests:**
    (Verify the setup and SDK functionality)
    ```bash
    uv run pytest
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

## Future Enhancements

*   **Response Models:** Introduce Pydantic models for API responses to provide a more object-oriented interface and stronger type guarantees.

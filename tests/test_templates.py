"""Tests for template-related operations in the Siren API client."""

import os
import sys

import pytest
import requests

# Ensure the 'siren' package in the parent directory can be imported:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# The 'client' fixture is automatically available from conftest.py


def test_get_templates_success(client, requests_mock):
    """Test successful retrieval of templates."""
    mock_response_data = {
        "data": {
            "content": [
                {"id": "tpl_1", "name": "Test Template 1"},
                {"id": "tpl_2", "name": "Test Template 2"},
            ],
            "totalElements": 2,
        }
    }
    requests_mock.get(
        f"{client._templates.base_url}/template",
        json=mock_response_data,
        status_code=200,
    )

    response = client.get_templates(page=0, size=10)
    assert response == mock_response_data
    assert len(response["data"]["content"]) == 2
    assert response["data"]["content"][0]["name"] == "Test Template 1"


def test_get_templates_http_error(client, requests_mock):
    """Test handling of HTTP error when getting templates."""
    error_response_data = {
        "error": {"errorCode": "UNAUTHORISED", "message": "Invalid API Key"}
    }
    requests_mock.get(
        f"{client._templates.base_url}/template",
        json=error_response_data,
        status_code=401,
    )

    response = client.get_templates()
    assert response == error_response_data


def test_get_templates_network_error(client, requests_mock):
    """Test handling of a network error when getting templates."""
    requests_mock.get(
        f"{client._templates.base_url}/template", exc=requests.exceptions.ConnectTimeout
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        client.get_templates()


def test_create_template_success(client, requests_mock):
    """Test successful creation of a template."""
    mock_request_payload = {
        "name": "Test_Create_Template",
        "description": "A test template for creation",
        "tagNames": ["test", "creation"],
        "variables": [{"name": "user_name", "defaultValue": "Guest"}],
        "configurations": {
            "EMAIL": {
                "subject": "Welcome {{user_name}}!",
                "channel": "EMAIL",
                "body": "<p>Hello {{user_name}}, welcome!</p>",
                "isRawHTML": True,
                "isPlainText": False,
            }
        },
    }
    mock_response_data = {
        "data": {
            "templateId": "tpl_abc123",
            "templateName": "Test_Create_Template",
            "draftVersionId": "ver_def456",
            "channelTemplateList": [
                {
                    "id": "ct_email_789",
                    "channel": "EMAIL",
                    "configuration": {"channel": "EMAIL"},
                    "templateVersionId": "ver_def456",
                }
            ],
        },
        "error": None,
        "errors": None,
        "meta": None,
    }
    requests_mock.post(
        f"{client._templates.base_url}/template",
        json=mock_response_data,
        status_code=200,
    )

    response = client.create_template(mock_request_payload)
    assert response == mock_response_data
    assert requests_mock.last_request.json() == mock_request_payload


def test_create_template_http_error(client, requests_mock):
    """Test handling of HTTP error when creating a template."""
    mock_request_payload = {"name": "Invalid Template"}
    error_response_data = {
        "data": None,
        "error": {"errorCode": "BAD_REQUEST", "message": "Bad request"},
        "errors": [
            {
                "errorCode": "BAD_REQUEST",
                "message": "Name is too short or missing fields",
            }
        ],
        "meta": None,
    }
    requests_mock.post(
        f"{client._templates.base_url}/template",
        json=error_response_data,
        status_code=400,
    )

    response = client.create_template(mock_request_payload)
    assert response == error_response_data


def test_create_template_network_error(client, requests_mock):
    """Test handling of a network error when creating a template."""
    mock_request_payload = {"name": "Network Error Template"}
    requests_mock.post(
        f"{client._templates.base_url}/template", exc=requests.exceptions.ConnectTimeout
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        client.create_template(mock_request_payload)


def test_update_template_success(client, requests_mock):
    """Test successful update of a template."""
    template_id = "tpl_xyz789"
    mock_request_payload = {
        "name": "Updated_Test_Template",
        "description": "An updated test template",
        "tagNames": ["updated", "test"],
        "variables": [{"name": "user_name", "defaultValue": "Updated Guest"}],
        "configurations": {
            "EMAIL": {
                "subject": "Updated Welcome {{user_name}}!",
                "channel": "EMAIL",
                "body": "<p>Hello {{user_name}}, your details are updated!</p>",
                "isRawHTML": True,
                "isPlainText": False,
            }
        },
    }
    mock_response_data = {
        "data": {
            "templateId": template_id,
            "templateName": "Updated_Test_Template",
            "draftVersionId": "ver_jkl012",
            "channelTemplateList": [
                {
                    "id": "ct_email_345",
                    "channel": "EMAIL",
                    "configuration": {"channel": "EMAIL"},
                    "templateVersionId": "ver_jkl012",
                }
            ],
        },
        "error": None,
        "errors": None,
        "meta": None,
    }
    requests_mock.put(
        f"{client._templates.base_url}/template/{template_id}",
        json=mock_response_data,
        status_code=200,
    )

    response = client.update_template(template_id, mock_request_payload)
    assert response == mock_response_data
    assert requests_mock.last_request.json() == mock_request_payload
    assert requests_mock.last_request.method == "PUT"


def test_update_template_http_error(client, requests_mock):
    """Test handling of HTTP error when updating a template."""
    template_id = "tpl_error400"
    mock_request_payload = {"name": "Invalid Update"}
    error_response_data = {
        "data": None,
        "error": {"errorCode": "BAD_REQUEST", "message": "Invalid data for update"},
        "errors": [
            {
                "errorCode": "BAD_REQUEST",
                "message": "Name is too short or some fields are invalid",
            }
        ],
        "meta": None,
    }
    requests_mock.put(
        f"{client._templates.base_url}/template/{template_id}",
        json=error_response_data,
        status_code=400,
    )

    response = client.update_template(template_id, mock_request_payload)
    assert response == error_response_data


def test_update_template_network_error(client, requests_mock):
    """Test handling of a network error when updating a template."""
    template_id = "tpl_network_err"
    mock_request_payload = {"name": "Network Error Update"}
    requests_mock.put(
        f"{client._templates.base_url}/template/{template_id}",
        exc=requests.exceptions.ConnectTimeout,
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        client.update_template(template_id, mock_request_payload)


def test_delete_template_success(client, requests_mock):
    """Test successful deletion of a template (204 No Content)."""
    template_id = "tpl_todelete123"
    expected_response_data = {
        "status": "success",
        "message": f"Template {template_id} deleted successfully.",
    }
    requests_mock.delete(
        f"{client._templates.base_url}/template/{template_id}",
        text="",  # Empty body for 204
        status_code=204,
    )

    response = client.delete_template(template_id)
    assert response == expected_response_data
    assert requests_mock.last_request.method == "DELETE"


def test_delete_template_not_found_error(client, requests_mock):
    """Test handling of a 404 Not Found error when deleting a template."""
    template_id = "tpl_notfound404"
    error_response_data = {
        "data": None,
        "error": {"errorCode": "NOT_FOUND", "message": "Template not found"},
        "errors": [
            {
                "errorCode": "NOT_FOUND",
                "message": f"Template with id {template_id} not found",
            }
        ],
        "meta": None,
    }
    requests_mock.delete(
        f"{client._templates.base_url}/template/{template_id}",
        json=error_response_data,
        status_code=404,
    )

    response = client.delete_template(template_id)
    assert response == error_response_data


def test_delete_template_unauthorized_error(client, requests_mock):
    """Test handling of a 401 Unauthorized error when deleting a template."""
    template_id = "tpl_unauth401"
    error_response_data = {
        "error": {"errorCode": "UNAUTHORISED", "message": "Invalid API Key"}
    }
    requests_mock.delete(
        f"{client._templates.base_url}/template/{template_id}",
        json=error_response_data,
        status_code=401,
    )

    response = client.delete_template(template_id)
    assert response == error_response_data


def test_delete_template_network_error(client, requests_mock):
    """Test handling of a network error when deleting a template."""
    template_id = "tpl_network_error"
    requests_mock.delete(
        f"{client._templates.base_url}/template/{template_id}",
        exc=requests.exceptions.ConnectTimeout,
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        client.delete_template(template_id)

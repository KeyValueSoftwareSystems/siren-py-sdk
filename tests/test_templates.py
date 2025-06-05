"""Tests for template-related operations in the Siren API client."""

import os
import sys

import pytest
import requests
from requests_mock import Mocker as RequestsMocker

# Ensure the 'siren' package in the parent directory can be imported:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# The 'client' fixture is automatically available from conftest.py


def test_get_templates_success(client, requests_mock: RequestsMocker):
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


def test_get_templates_http_error(client, requests_mock: RequestsMocker):
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


def test_get_templates_network_error(client, requests_mock: RequestsMocker):
    """Test handling of a network error when getting templates."""
    requests_mock.get(
        f"{client._templates.base_url}/template", exc=requests.exceptions.ConnectTimeout
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        client.get_templates()


def test_get_templates_http_error_non_json_response(
    client, requests_mock: RequestsMocker
):
    """Test HTTP error with non-JSON response for get_templates."""
    requests_mock.get(
        f"{client._templates.base_url}/template",
        text="Service Unavailable - Not JSON",
        status_code=503,
    )

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        client.get_templates()

    assert exc_info.value.response.status_code == 503
    assert exc_info.value.response.text == "Service Unavailable - Not JSON"


def test_create_template_success(client, requests_mock: RequestsMocker):
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
    assert requests_mock.last_request is not None
    assert requests_mock.last_request.json() == mock_request_payload


def test_create_template_http_error(client, requests_mock: RequestsMocker):
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


def test_create_template_network_error(client, requests_mock: RequestsMocker):
    """Test handling of a network error when creating a template."""
    mock_request_payload = {"name": "Network Error Template"}
    requests_mock.post(
        f"{client._templates.base_url}/template", exc=requests.exceptions.ConnectTimeout
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        client.create_template(mock_request_payload)


def test_create_template_http_error_non_json_response(
    client, requests_mock: RequestsMocker
):
    """Test HTTP error with non-JSON response for create_template."""
    mock_request_payload = {"name": "Test Non-JSON Error"}
    requests_mock.post(
        f"{client._templates.base_url}/template",
        text="Server Error - Not JSON",
        status_code=500,
    )

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        client.create_template(mock_request_payload)

    assert exc_info.value.response.status_code == 500
    assert exc_info.value.response.text == "Server Error - Not JSON"


def test_update_template_success(client, requests_mock: RequestsMocker):
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
    assert requests_mock.last_request is not None
    assert requests_mock.last_request.json() == mock_request_payload
    assert requests_mock.last_request.method == "PUT"


def test_update_template_http_error(client, requests_mock: RequestsMocker):
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


def test_update_template_network_error(client, requests_mock: RequestsMocker):
    """Test handling of a network error when updating a template."""
    template_id = "tpl_network_err"
    mock_request_payload = {"name": "Network Error Update"}
    requests_mock.put(
        f"{client._templates.base_url}/template/{template_id}",
        exc=requests.exceptions.ConnectTimeout,
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        client.update_template(template_id, mock_request_payload)


def test_update_template_http_error_non_json_response(
    client, requests_mock: RequestsMocker
):
    """Test HTTP error with non-JSON response for update_template."""
    template_id = "tpl_non_json_error"
    mock_request_payload = {"name": "Test Update Non-JSON Error"}
    requests_mock.put(
        f"{client._templates.base_url}/template/{template_id}",
        text="Internal Server Error - Not JSON",
        status_code=500,
    )

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        client.update_template(template_id, mock_request_payload)

    assert exc_info.value.response.status_code == 500
    assert exc_info.value.response.text == "Internal Server Error - Not JSON"


def test_delete_template_success(client, requests_mock: RequestsMocker):
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
    assert requests_mock.last_request is not None
    assert requests_mock.last_request.method == "DELETE"


def test_delete_template_not_found_error(client, requests_mock: RequestsMocker):
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


def test_delete_template_unauthorized_error(client, requests_mock: RequestsMocker):
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


def test_delete_template_network_error(client, requests_mock: RequestsMocker):
    """Test handling of a network error when deleting a template."""
    template_id = "tpl_network_error"
    requests_mock.delete(
        f"{client._templates.base_url}/template/{template_id}",
        exc=requests.exceptions.ConnectTimeout,
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        client.delete_template(template_id)


def test_delete_template_http_error_non_json_response(
    client, requests_mock: RequestsMocker
):
    """Test HTTP error with non-JSON response for delete_template."""
    template_id = "tpl_non_json_delete_error"
    requests_mock.delete(
        f"{client._templates.base_url}/template/{template_id}",
        text="Gateway Timeout - Not JSON",
        status_code=504,
    )

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        client.delete_template(template_id)

    assert exc_info.value.response.status_code == 504
    assert exc_info.value.response.text == "Gateway Timeout - Not JSON"


def test_publish_template_success(client, requests_mock: RequestsMocker):
    """Test successful publishing of a template."""
    template_id = "tpl_pub_success"
    mock_response_data = {
        "data": {
            "id": template_id,
            "name": "Published Template",
            "publishedVersion": {"status": "PUBLISHED_LATEST"},
        },
        "error": None,
    }
    requests_mock.patch(
        f"{client._templates.base_url}/template/{template_id}/publish",
        json=mock_response_data,
        status_code=200,
    )

    response = client.publish_template(template_id)
    assert response == mock_response_data
    assert requests_mock.last_request is not None
    assert requests_mock.last_request.method == "PATCH"


def test_publish_template_not_found_error(client, requests_mock: RequestsMocker):
    """Test handling of a 404 Not Found error when publishing a template."""
    template_id = "tpl_pub_notfound"
    error_response_data = {
        "data": None,
        "error": {"errorCode": "NOT_FOUND", "message": "Template not found"},
        "errors": [{"errorCode": "NOT_FOUND", "message": "Template not found"}],
        "meta": None,
    }
    requests_mock.patch(
        f"{client._templates.base_url}/template/{template_id}/publish",
        json=error_response_data,
        status_code=404,
    )

    response = client.publish_template(template_id)
    assert response == error_response_data


def test_publish_template_unauthorized_error(client, requests_mock: RequestsMocker):
    """Test handling of a 401 Unauthorized error when publishing a template."""
    template_id = "tpl_pub_unauth"
    error_response_data = {
        "data": None,
        "error": {"errorCode": "UNAUTHORISED", "message": "Invalid API Key"},
        "errors": [{"errorCode": "UNAUTHORISED", "message": "Invalid API Key"}],
        "meta": None,
    }
    requests_mock.patch(
        f"{client._templates.base_url}/template/{template_id}/publish",
        json=error_response_data,
        status_code=401,
    )

    response = client.publish_template(template_id)
    assert response == error_response_data


def test_publish_template_bad_request_error(client, requests_mock: RequestsMocker):
    """Test handling of a 400 Bad Request error when publishing a template."""
    template_id = "tpl_pub_badreq"
    error_response_data = {
        "data": None,
        "error": {
            "errorCode": "BAD_REQUEST",
            "message": "Template has no versions to publish",
        },
        "errors": [
            {
                "errorCode": "BAD_REQUEST",
                "message": "Template has no versions to publish",
            }
        ],
        "meta": None,
    }
    requests_mock.patch(
        f"{client._templates.base_url}/template/{template_id}/publish",
        json=error_response_data,
        status_code=400,
    )

    response = client.publish_template(template_id)
    assert response == error_response_data


def test_publish_template_network_error(client, requests_mock: RequestsMocker):
    """Test handling of a network error when publishing a template."""
    template_id = "tpl_pub_network_err"
    requests_mock.patch(
        f"{client._templates.base_url}/template/{template_id}/publish",
        exc=requests.exceptions.ConnectTimeout,
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        client.publish_template(template_id)


def test_publish_template_http_error_non_json_response(
    client, requests_mock: RequestsMocker
):
    """Test HTTP error with non-JSON response for publish_template."""
    template_id = "tpl_non_json_publish_error"
    requests_mock.patch(
        f"{client._templates.base_url}/template/{template_id}/publish",
        text="Bad Gateway - Not JSON",
        status_code=502,
    )

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        client.publish_template(template_id)

    assert exc_info.value.response.status_code == 502
    assert exc_info.value.response.text == "Bad Gateway - Not JSON"


def test_create_channel_configurations_success(client, requests_mock: RequestsMocker):
    """Test successful creation of channel configurations."""
    template_id = "tpl_test123"
    mock_request_payload = {
        "SMS": {
            "body": "Test SMS body for channel config",
            "channel": "SMS",
            "isFlash": False,
            "isUnicode": False,
        },
        "EMAIL": {
            "subject": "Test Email Subject for channel config",
            "channel": "EMAIL",
            "body": "<p>Test Email Body for channel config</p>",
            "attachments": [],
            "isRawHTML": True,
            "isPlainText": False,
        },
    }
    mock_response_data = {
        "data": mock_request_payload,  # Assuming API returns the created configs in 'data'
        "error": None,
        "errors": None,
        "meta": None,
    }
    requests_mock.post(
        f"{client._templates.base_url}/template/{template_id}/channel-templates",
        json=mock_response_data,
        status_code=200,
    )

    response = client.create_channel_configurations(template_id, mock_request_payload)
    assert response == mock_response_data
    assert requests_mock.last_request is not None
    assert requests_mock.last_request.json() == mock_request_payload
    assert requests_mock.last_request.method == "POST"


def test_create_channel_configurations_bad_request(
    client, requests_mock: RequestsMocker
):
    """Test handling of a 400 Bad Request error for channel configurations."""
    template_id = "tpl_badreq400"
    mock_request_payload = {"INVALID_CHANNEL": {"body": "invalid"}}
    error_response_data = {
        "data": None,
        "error": {
            "errorCode": "BAD_REQUEST",
            "message": "Invalid channel configuration provided.",
        },
        "errors": [
            {
                "errorCode": "BAD_REQUEST",
                "message": "Channel type INVALID_CHANNEL not supported.",
            }
        ],
        "meta": None,
    }
    requests_mock.post(
        f"{client._templates.base_url}/template/{template_id}/channel-templates",
        json=error_response_data,
        status_code=400,
    )

    response = client.create_channel_configurations(template_id, mock_request_payload)
    assert response == error_response_data


def test_create_channel_configurations_unauthorized(
    client, requests_mock: RequestsMocker
):
    """Test handling of a 401 Unauthorized error for channel configurations."""
    template_id = "tpl_unauth401"
    mock_request_payload = {"SMS": {"body": "test"}}
    error_response_data = {
        "data": None,
        "error": {"errorCode": "UNAUTHORISED", "message": "Authentication required."},
        "errors": [
            {
                "errorCode": "UNAUTHORISED",
                "message": "Valid API key is missing or invalid.",
            }
        ],
        "meta": None,
    }
    requests_mock.post(
        f"{client._templates.base_url}/template/{template_id}/channel-templates",
        json=error_response_data,
        status_code=401,
    )

    response = client.create_channel_configurations(template_id, mock_request_payload)
    assert response == error_response_data


def test_create_channel_configurations_not_found(client, requests_mock: RequestsMocker):
    """Test handling of a 404 Not Found error (template_id) for channel configurations."""
    template_id = "tpl_notfound404"
    mock_request_payload = {"SMS": {"body": "test"}}
    error_response_data = {
        "data": None,
        "error": {
            "errorCode": "NOT_FOUND",
            "message": f"Template with id {template_id} not found.",
        },
        "errors": [
            {
                "errorCode": "NOT_FOUND",
                "message": "The requested template does not exist.",
            }
        ],
        "meta": None,
    }
    requests_mock.post(
        f"{client._templates.base_url}/template/{template_id}/channel-templates",
        json=error_response_data,
        status_code=404,
    )

    response = client.create_channel_configurations(template_id, mock_request_payload)
    assert response == error_response_data


def test_create_channel_configurations_network_error(
    client, requests_mock: RequestsMocker
):
    """Test handling of a network error for channel configurations."""
    template_id = "tpl_network_error"
    mock_request_payload = {"SMS": {"body": "test"}}
    requests_mock.post(
        f"{client._templates.base_url}/template/{template_id}/channel-templates",
        exc=requests.exceptions.ConnectTimeout,
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        client.create_channel_configurations(template_id, mock_request_payload)


def test_create_channel_configurations_http_error_non_json_response(
    client, requests_mock
):
    """Test HTTP error with non-JSON response for channel configurations."""
    template_id = "tpl_non_json_error"
    mock_request_payload = {
        "EMAIL": {"subject": "Test", "body": "Body", "channel": "EMAIL"}
    }
    requests_mock.post(
        f"{client._templates.base_url}/template/{template_id}/channel-templates",
        text="<HTML><BODY>Internal Server Error</BODY></HTML>",
        status_code=500,
    )

    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        client.create_channel_configurations(template_id, mock_request_payload)
    assert "500 Server Error" in str(excinfo.value)
    assert (
        "<HTML><BODY>Internal Server Error</BODY></HTML>" in excinfo.value.response.text
    )


def test_get_channel_templates_success(client, requests_mock: RequestsMocker):
    """Test successful retrieval of channel templates for a version."""
    version_id = "ver_123xyz"
    mock_response_data = {
        "data": {
            "content": [
                {"channel": "SMS", "configuration": {"channel": "SMS"}},
                {"channel": "EMAIL", "configuration": {"channel": "EMAIL"}},
            ],
            "totalElements": 2,
        }
    }
    requests_mock.get(
        f"{client._templates.base_url}/template/versions/{version_id}/channel-templates",
        json=mock_response_data,
        status_code=200,
    )

    response = client.get_channel_templates(version_id=version_id)
    assert response == mock_response_data
    assert len(response["data"]["content"]) == 2
    assert requests_mock.last_request is not None
    assert requests_mock.last_request.qs == {}


def test_get_channel_templates_success_with_params(
    client, requests_mock: RequestsMocker
):
    """Test successful retrieval of channel templates with query parameters."""
    version_id = "ver_456abc"
    mock_response_data = {
        "data": {"content": [{"channel": "PUSH", "configuration": {"channel": "PUSH"}}]}
    }
    requests_mock.get(
        f"{client._templates.base_url}/template/versions/{version_id}/channel-templates",
        json=mock_response_data,
        status_code=200,
    )

    response = client.get_channel_templates(
        version_id=version_id,
        channel="PUSH",
        search="config_detail",
        sort="channel,asc",
        page=1,
        size=5,
    )
    assert response == mock_response_data
    assert requests_mock.last_request is not None
    assert requests_mock.last_request.qs == {
        "channel": ["push"],  # Changed to lowercase
        "search": ["config_detail"],
        "sort": ["channel,asc"],
        "page": ["1"],
        "size": ["5"],
    }


def test_get_channel_templates_bad_request_error(client, requests_mock: RequestsMocker):
    """Test 400 Bad Request error for get_channel_templates."""
    version_id = "ver_invalid_format"
    error_response_data = {
        "error": {"errorCode": "BAD_REQUEST", "message": "Invalid version ID format"}
    }
    requests_mock.get(
        f"{client._templates.base_url}/template/versions/{version_id}/channel-templates",
        json=error_response_data,
        status_code=400,
    )
    response = client.get_channel_templates(version_id=version_id)
    assert response == error_response_data


def test_get_channel_templates_unauthorized_error(
    client, requests_mock: RequestsMocker
):
    """Test 401 Unauthorized error for get_channel_templates."""
    version_id = "ver_789def"
    error_response_data = {
        "error": {"errorCode": "UNAUTHORISED", "message": "Invalid API Key"}
    }
    requests_mock.get(
        f"{client._templates.base_url}/template/versions/{version_id}/channel-templates",
        json=error_response_data,
        status_code=401,
    )
    response = client.get_channel_templates(version_id=version_id)
    assert response == error_response_data


def test_get_channel_templates_not_found_error(client, requests_mock: RequestsMocker):
    """Test 404 Not Found error for get_channel_templates."""
    version_id = "ver_not_exists"
    error_response_data = {
        "error": {"errorCode": "NOT_FOUND", "message": "Version not found"}
    }
    requests_mock.get(
        f"{client._templates.base_url}/template/versions/{version_id}/channel-templates",
        json=error_response_data,
        status_code=404,
    )
    response = client.get_channel_templates(version_id=version_id)
    assert response == error_response_data


def test_get_channel_templates_network_error(client, requests_mock: RequestsMocker):
    """Test network error for get_channel_templates."""
    version_id = "ver_network_issue"
    requests_mock.get(
        f"{client._templates.base_url}/template/versions/{version_id}/channel-templates",
        exc=requests.exceptions.ConnectionError,
    )
    with pytest.raises(requests.exceptions.ConnectionError):
        client.get_channel_templates(version_id=version_id)


def test_get_channel_templates_http_error_non_json_response(
    client, requests_mock: RequestsMocker
):
    """Test HTTP error with non-JSON response for get_channel_templates."""
    version_id = "ver_html_error"
    requests_mock.get(
        f"{client._templates.base_url}/template/versions/{version_id}/channel-templates",
        text="<HTML><BODY>Internal Server Error</BODY></HTML>",
        status_code=500,
    )
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        client.get_channel_templates(version_id=version_id)
    assert "500 Server Error" in str(excinfo.value)
    assert (
        "<HTML><BODY>Internal Server Error</BODY></HTML>" in excinfo.value.response.text
    )

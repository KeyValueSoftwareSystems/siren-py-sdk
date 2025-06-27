"""Unit tests for the templates client using BaseClient."""

from unittest.mock import Mock, patch

import pytest

from siren.clients.templates import TemplateClient
from siren.exceptions import SirenAPIError, SirenSDKError
from siren.models.templates import CreatedTemplate, Template

API_KEY = "test_api_key"
BASE_URL = "https://api.dev.trysiren.io"


def mock_response(status_code: int, json_data: dict = None):
    """Helper function to create a mock HTTP response."""
    mock_resp = Mock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data if json_data is not None else {}
    return mock_resp


class TestTemplateClient:
    """Tests for the TemplateClient class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = TemplateClient(api_key=API_KEY, base_url=BASE_URL)

    @patch("siren.clients.base.requests.request")
    def test_get_templates_success(self, mock_request):
        """Test successful retrieval of templates."""
        # Mock API response based on user-provided response
        mock_api_response = {
            "data": [
                {
                    "id": "cacf1503-8283-42a8-b5fd-27d85054fb99",
                    "name": "test1",
                    "variables": [],
                    "tags": [],
                    "draftVersion": {
                        "id": "568a2903-056c-43ba-bc4f-cce420fb1ced",
                        "version": 1,
                        "status": "DRAFT",
                        "publishedAt": None,
                    },
                    "templateVersions": [
                        {
                            "id": "568a2903-056c-43ba-bc4f-cce420fb1ced",
                            "version": 1,
                            "status": "DRAFT",
                            "publishedAt": None,
                        }
                    ],
                },
                {
                    "id": "11921404-4517-48b7-82ee-fcdcf8f9c03b",
                    "name": "jithu_test1",
                    "variables": [],
                    "tags": ["sampleTag", "tag2"],
                    "draftVersion": {
                        "id": "dd8d8a77-7fcf-4bd8-8d8b-89f1e5e8822a",
                        "version": 2,
                        "status": "DRAFT",
                        "publishedAt": None,
                    },
                    "publishedVersion": {
                        "id": "9138125c-d242-4b17-ae0e-16ade9d06568",
                        "version": 1,
                        "status": "PUBLISHED_LATEST",
                        "publishedAt": "2025-06-05T10:39:53.780+00:00",
                    },
                    "templateVersions": [
                        {
                            "id": "9138125c-d242-4b17-ae0e-16ade9d06568",
                            "version": 1,
                            "status": "PUBLISHED_LATEST",
                            "publishedAt": "2025-06-05T10:39:53.780+00:00",
                        }
                    ],
                },
            ],
            "error": None,
            "meta": {
                "last": "false",
                "totalPages": "2",
                "pageSize": "2",
                "currentPage": "0",
                "first": "true",
                "totalElements": "3",
            },
        }
        mock_request.return_value = mock_response(200, mock_api_response)

        # Call the method
        result = self.client.get(page=0, size=2)

        # Verify result is List[Template]
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(template, Template) for template in result)

        # Verify first template
        first_template = result[0]
        assert first_template.id == "cacf1503-8283-42a8-b5fd-27d85054fb99"
        assert first_template.name == "test1"
        assert first_template.tags == []
        assert first_template.draft_version.status == "DRAFT"
        assert first_template.published_version is None

        # Verify second template
        second_template = result[1]
        assert second_template.id == "11921404-4517-48b7-82ee-fcdcf8f9c03b"
        assert second_template.name == "jithu_test1"
        assert second_template.tags == ["sampleTag", "tag2"]
        assert second_template.draft_version.status == "DRAFT"
        assert second_template.published_version.status == "PUBLISHED_LATEST"

        # Verify request was made correctly with BaseClient
        mock_request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/api/v1/public/template",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json=None,
            params={"page": 0, "size": 2},
            timeout=10,
        )

    @patch("siren.clients.base.requests.request")
    def test_get_templates_with_all_params(self, mock_request):
        """Test get_templates with all optional parameters."""
        mock_api_response = {
            "data": [],
            "error": None,
            "meta": {
                "last": "true",
                "totalPages": "0",
                "pageSize": "5",
                "currentPage": "0",
                "first": "true",
                "totalElements": "0",
            },
        }
        mock_request.return_value = mock_response(200, mock_api_response)

        # Call with all parameters
        result = self.client.get(
            tag_names="test,example", search="template", sort="name,asc", page=1, size=5
        )

        assert isinstance(result, list)
        assert len(result) == 0

        # Verify all parameters were passed correctly
        mock_request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/api/v1/public/template",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json=None,
            params={
                "tagNames": "test,example",
                "search": "template",
                "sort": "name,asc",
                "page": 1,
                "size": 5,
            },
            timeout=10,
        )

    @patch("siren.clients.base.requests.request")
    def test_get_templates_api_error(self, mock_request):
        """Test API error during template retrieval."""
        mock_api_error = {
            "error": {"errorCode": "UNAUTHORIZED", "message": "Invalid API key"}
        }
        mock_request.return_value = mock_response(401, mock_api_error)

        with pytest.raises(SirenAPIError) as exc_info:
            self.client.get()

        assert exc_info.value.error_code == "UNAUTHORIZED"
        assert "Invalid API key" in exc_info.value.api_message

    @patch("siren.clients.base.requests.request")
    def test_get_templates_network_error(self, mock_request):
        """Test network error during template retrieval."""
        from requests.exceptions import ConnectionError

        mock_request.side_effect = ConnectionError("Connection failed")

        with pytest.raises(SirenSDKError) as exc_info:
            self.client.get()

        assert "Connection failed" in exc_info.value.message

    @patch("siren.clients.base.requests.request")
    def test_create_template_success(self, mock_request):
        """Test successful template creation."""
        mock_api_response = {
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
        }
        mock_request.return_value = mock_response(200, mock_api_response)

        result = self.client.create(
            name="Test_Create_Template",
            description="A test template",
            tag_names=["test", "creation"],
            variables=[{"name": "user_name", "defaultValue": "Guest"}],
            configurations={
                "EMAIL": {
                    "subject": "Welcome {{user_name}}!",
                    "channel": "EMAIL",
                    "body": "<p>Hello {{user_name}}, welcome!</p>",
                    "isRawHTML": True,
                    "isPlainText": False,
                }
            },
        )

        assert isinstance(result, CreatedTemplate)
        assert result.template_id == "tpl_abc123"
        assert result.template_name == "Test_Create_Template"
        assert result.draft_version_id == "ver_def456"
        assert len(result.channel_template_list) == 1
        assert result.channel_template_list[0].channel == "EMAIL"

        # Verify request with camelCase conversion
        mock_request.assert_called_once_with(
            method="POST",
            url=f"{BASE_URL}/api/v1/public/template",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "name": "Test_Create_Template",
                "description": "A test template",
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
            },
            params=None,
            timeout=10,
        )

    @patch("siren.clients.base.requests.request")
    def test_create_template_api_error(self, mock_request):
        """Test API error during template creation."""
        mock_api_error = {
            "error": {"errorCode": "BAD_REQUEST", "message": "Bad request"}
        }
        mock_request.return_value = mock_response(400, mock_api_error)

        with pytest.raises(SirenAPIError) as exc_info:
            self.client.create(name="Invalid Template")

        assert exc_info.value.error_code == "BAD_REQUEST"
        assert "Bad request" in exc_info.value.api_message

    @patch("siren.clients.base.requests.request")
    def test_delete_template_success(self, mock_request):
        """Test successful template deletion (204 No Content)."""
        # Mock 204 response with empty body
        mock_request.return_value = mock_response(204, "")

        template_id = "tpl_delete_123"
        result = self.client.delete(template_id)

        assert result is True

        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method="DELETE",
            url=f"{BASE_URL}/api/v1/public/template/{template_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json=None,
            params=None,
            timeout=10,
        )

    @patch("siren.clients.base.requests.request")
    def test_delete_template_not_found(self, mock_request):
        """Test template deletion with 404 error."""
        mock_api_error = {
            "error": {"errorCode": "NOT_FOUND", "message": "Template not found"}
        }
        mock_request.return_value = mock_response(404, mock_api_error)

        template_id = "tpl_not_found"

        with pytest.raises(SirenAPIError) as exc_info:
            self.client.delete(template_id)

        assert exc_info.value.error_code == "NOT_FOUND"
        assert "Template not found" in exc_info.value.api_message

    @patch("siren.clients.base.requests.request")
    def test_update_template_success(self, mock_request):
        """Test successful template update."""
        mock_api_response = {
            "data": {
                "id": "tpl_xyz789",
                "name": "Updated_Test_Template",
                "variables": [],
                "tags": ["updated", "test"],
                "draftVersion": {
                    "id": "ver_jkl012",
                    "version": 2,
                    "status": "DRAFT",
                    "publishedAt": None,
                },
                "templateVersions": [],
            },
            "error": None,
        }
        mock_request.return_value = mock_response(200, mock_api_response)

        template_id = "tpl_xyz789"

        result = self.client.update(
            template_id,
            name="Updated_Test_Template",
            description="An updated test template",
            tag_names=["updated", "test"],
            variables=[{"name": "user_name", "defaultValue": "Updated Guest"}],
        )

        assert isinstance(result, Template)
        assert result.id == "tpl_xyz789"
        assert result.name == "Updated_Test_Template"

        # Verify request with camelCase conversion
        mock_request.assert_called_once_with(
            method="PUT",
            url=f"{BASE_URL}/api/v1/public/template/{template_id}",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "name": "Updated_Test_Template",
                "description": "An updated test template",
                "tagNames": ["updated", "test"],
                "variables": [{"name": "user_name", "defaultValue": "Updated Guest"}],
            },
            params=None,
            timeout=10,
        )

    @patch("siren.clients.base.requests.request")
    def test_publish_template_success(self, mock_request):
        """Test successful template publishing."""
        template_id = "tpl_pub_success"
        mock_api_response = {
            "data": {
                "id": template_id,
                "name": "Published Template",
                "variables": [],
                "tags": [],
                "draftVersion": {
                    "id": "ver_draft_123",
                    "version": 2,
                    "status": "DRAFT",
                    "publishedAt": None,
                },
                "publishedVersion": {
                    "id": "ver_pub_456",
                    "version": 1,
                    "status": "PUBLISHED_LATEST",
                    "publishedAt": "2025-01-15T10:00:00.000+00:00",
                },
                "templateVersions": [],
            },
            "error": None,
        }
        mock_request.return_value = mock_response(200, mock_api_response)

        result = self.client.publish(template_id)

        assert isinstance(result, Template)
        assert result.id == template_id
        assert result.name == "Published Template"
        assert result.published_version is not None
        assert result.published_version.status == "PUBLISHED_LATEST"

        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method="PATCH",
            url=f"{BASE_URL}/api/v1/public/template/{template_id}/publish",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json=None,
            params=None,
            timeout=10,
        )

    @patch("siren.clients.base.requests.request")
    def test_publish_template_not_found(self, mock_request):
        """Test template publishing with 404 error."""
        template_id = "tpl_not_found"
        mock_api_error = {
            "error": {"errorCode": "NOT_FOUND", "message": "Template not found"}
        }
        mock_request.return_value = mock_response(404, mock_api_error)

        with pytest.raises(SirenAPIError) as exc_info:
            self.client.publish(template_id)

        assert exc_info.value.error_code == "NOT_FOUND"
        assert "Template not found" in exc_info.value.api_message

    @patch("siren.clients.base.requests.request")
    def test_publish_template_bad_request(self, mock_request):
        """Test template publishing with 400 error."""
        template_id = "tpl_bad_request"
        mock_api_error = {
            "error": {
                "errorCode": "BAD_REQUEST",
                "message": "Template has no versions to publish",
            }
        }
        mock_request.return_value = mock_response(400, mock_api_error)

        with pytest.raises(SirenAPIError) as exc_info:
            self.client.publish(template_id)

        assert exc_info.value.error_code == "BAD_REQUEST"
        assert "Template has no versions to publish" in exc_info.value.api_message

    @patch("siren.clients.base.requests.request")
    def test_create_channel_templates_success(self, mock_request):
        """Test successful creation of channel templates."""
        mock_input_data = {
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
        # API returns a list of ChannelTemplate objects
        mock_response_data = {
            "data": [
                {
                    "channel": "SMS",
                    "configuration": {
                        "channel": "SMS",
                        "body": "Test SMS body for channel config",
                        "isFlash": False,
                        "isUnicode": False,
                    },
                },
                {
                    "channel": "EMAIL",
                    "configuration": {
                        "channel": "EMAIL",
                        "subject": "Test Email Subject for channel config",
                        "body": "<p>Test Email Body for channel config</p>",
                        "attachments": [],
                        "isRawHTML": True,
                        "isPlainText": False,
                    },
                },
            ],
            "error": None,
            "errors": None,
            "meta": None,
        }
        mock_request.return_value = mock_response(200, mock_response_data)

        result = self.client.create_channel_templates("template123", **mock_input_data)

        assert len(result) == 2
        assert result[0].channel == "SMS"
        assert result[1].channel == "EMAIL"
        mock_request.assert_called_once_with(
            method="POST",
            url=f"{BASE_URL}/api/v1/public/template/template123/channel-templates",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json=mock_input_data,
            params=None,
            timeout=10,
        )

    @patch("siren.clients.base.requests.request")
    def test_create_channel_templates_api_error(self, mock_request):
        """Test API error during channel templates creation."""
        mock_api_error = {
            "error": {
                "errorCode": "BAD_REQUEST",
                "message": "Invalid channel configuration",
            }
        }
        mock_request.return_value = mock_response(400, mock_api_error)

        with pytest.raises(SirenAPIError) as exc_info:
            self.client.create_channel_templates(
                "template123", SMS={"body": "test"}, INVALID_CHANNEL={"body": "invalid"}
            )

        assert exc_info.value.error_code == "BAD_REQUEST"
        assert "Invalid channel configuration" in exc_info.value.api_message

    @patch("siren.clients.base.requests.request")
    def test_get_channel_templates_success(self, mock_request):
        """Test successful retrieval of channel templates."""
        mock_response_data = {
            "data": [
                {
                    "channel": "SMS",
                    "configuration": {
                        "channel": "SMS",
                        "body": "Test SMS body",
                        "isFlash": False,
                        "isUnicode": False,
                    },
                },
                {
                    "channel": "EMAIL",
                    "configuration": {
                        "channel": "EMAIL",
                        "subject": "Test Email Subject",
                        "body": "<p>Test Email Body</p>",
                        "isRawHTML": True,
                        "isPlainText": False,
                    },
                },
            ],
            "error": None,
            "errors": None,
            "meta": None,
        }
        mock_request.return_value = mock_response(200, mock_response_data)

        result = self.client.get_channel_templates("version123")

        assert len(result) == 2
        assert result[0].channel == "SMS"
        assert result[1].channel == "EMAIL"
        mock_request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/api/v1/public/template/versions/version123/channel-templates",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json=None,
            params={},
            timeout=10,
        )

    @patch("siren.clients.base.requests.request")
    def test_get_channel_templates_with_params(self, mock_request):
        """Test get channel templates with query parameters."""
        mock_response_data = {
            "data": [
                {
                    "channel": "EMAIL",
                    "configuration": {
                        "channel": "EMAIL",
                        "subject": "Filtered Email",
                        "body": "<p>Filtered content</p>",
                    },
                },
            ],
            "error": None,
            "errors": None,
            "meta": None,
        }
        mock_request.return_value = mock_response(200, mock_response_data)

        result = self.client.get_channel_templates(
            "version123", channel="EMAIL", page=0, size=5
        )

        assert len(result) == 1
        assert result[0].channel == "EMAIL"
        mock_request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/api/v1/public/template/versions/version123/channel-templates",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json=None,
            params={"channel": "EMAIL", "page": 0, "size": 5},
            timeout=10,
        )

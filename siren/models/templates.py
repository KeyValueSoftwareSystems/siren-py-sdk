"""Template-related models for the Siren SDK."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .base import BaseAPIResponse


class TemplateVersion(BaseModel):
    """Template version information."""

    model_config = ConfigDict(validate_by_name=True)

    id: str
    version: int
    status: str
    published_at: Optional[str] = Field(None, alias="publishedAt")


class Template(BaseModel):
    """Template model matching API response structure."""

    model_config = ConfigDict(validate_by_name=True)

    id: str
    name: str
    variables: List[Dict[str, Any]] = []
    tags: List[str] = []
    draft_version: Optional[TemplateVersion] = Field(None, alias="draftVersion")
    published_version: Optional[TemplateVersion] = Field(None, alias="publishedVersion")
    template_versions: List[TemplateVersion] = Field(
        default_factory=list, alias="templateVersions"
    )


class TemplateListMeta(BaseModel):
    """Pagination metadata for template list."""

    last: str
    total_pages: str = Field(alias="totalPages")
    page_size: str = Field(alias="pageSize")
    current_page: str = Field(alias="currentPage")
    first: str
    total_elements: str = Field(alias="totalElements")


class ChannelTemplate(BaseModel):
    """Channel template within a created template."""

    model_config = ConfigDict(validate_by_name=True)

    id: Optional[str] = None
    channel: str
    configuration: Dict[str, Any]
    template_version_id: Optional[str] = Field(None, alias="templateVersionId")


class CreatedTemplate(BaseModel):
    """Created template response data."""

    model_config = ConfigDict(validate_by_name=True)

    template_id: str = Field(alias="templateId")
    template_name: str = Field(alias="templateName")
    draft_version_id: str = Field(alias="draftVersionId")
    channel_template_list: List[ChannelTemplate] = Field(
        default_factory=list, alias="channelTemplateList"
    )


class CreateTemplateRequest(BaseModel):
    """Request model for creating templates."""

    model_config = ConfigDict(validate_by_name=True)

    name: str
    description: Optional[str] = None
    tag_names: List[str] = Field(default_factory=list, alias="tagNames")
    variables: List[Dict[str, Any]] = Field(default_factory=list)
    configurations: Dict[str, Any] = Field(default_factory=dict)


class TemplateListResponse(BaseAPIResponse[List[Template]]):
    """API response for template list operations."""

    pass


class UpdateTemplateRequest(BaseModel):
    """Request model for updating templates."""

    model_config = ConfigDict(validate_by_name=True)

    name: Optional[str] = None
    description: Optional[str] = None
    tag_names: Optional[List[str]] = Field(None, alias="tagNames")
    variables: Optional[List[Dict[str, Any]]] = None
    configurations: Optional[Dict[str, Any]] = None


class CreateTemplateResponse(BaseAPIResponse[CreatedTemplate]):
    """API response for create template operations."""

    pass


class UpdateTemplateResponse(BaseAPIResponse[Template]):
    """API response for update template operations."""

    pass


class PublishTemplateResponse(BaseAPIResponse[Template]):
    """Response model for publish template API."""

    pass


class CreateChannelTemplatesRequest(BaseModel):
    """Request model for create channel templates operations.

    This is a flexible model that accepts any key-value pairs where
    keys are channel names and values are channel configurations.
    """

    model_config = ConfigDict(extra="allow")


class CreateChannelTemplatesResponse(BaseAPIResponse[List[ChannelTemplate]]):
    """Response model for create channel templates operations."""

    pass


class GetChannelTemplatesResponse(BaseAPIResponse[List[ChannelTemplate]]):
    """Response model for get channel templates operations."""

    pass

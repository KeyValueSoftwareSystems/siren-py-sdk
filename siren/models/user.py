"""Pydantic models for Siren User API resources."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from .base import BaseAPIResponse


class UserBase(BaseModel):
    """Base model with common user fields."""

    unique_id: Optional[str] = Field(None, alias="uniqueId")
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    reference_id: Optional[str] = Field(None, alias="referenceId")
    whatsapp: Optional[str] = None
    active_channels: Optional[List[str]] = Field(None, alias="activeChannels")
    active: Optional[bool] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

    class Config:
        """Pydantic model configuration."""

        populate_by_name = True
        extra = "ignore"


class UserRequest(UserBase):
    """Request model for creating or updating a user."""

    pass


class User(UserBase):
    """Represents a user object in the Siren system."""

    id: Optional[str] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
    avatar_url: Optional[HttpUrl] = Field(None, alias="avatarUrl")

    sms: Optional[str] = None
    push_token: Optional[str] = Field(None, alias="pushToken")
    in_app: Optional[bool] = Field(None, alias="inApp")
    slack: Optional[str] = None
    discord: Optional[str] = None
    teams: Optional[str] = None
    line: Optional[str] = None

    custom_data: Optional[Dict[str, Any]] = Field(None, alias="customData")
    segments: Optional[List[str]] = None


class UserAPIResponse(BaseAPIResponse[User]):
    """Specific API response structure for operations returning a User."""

    pass

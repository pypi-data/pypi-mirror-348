"""Tenant models for the MontyCloud SDK."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TenantDetails(BaseModel):
    """Details of a tenant."""

    id: Optional[str] = Field(None, alias="ID")
    name: str = Field(alias="Name")
    description: Optional[str] = Field(None, alias="Description")
    parent_tenant_id: Optional[str] = Field(None, alias="ParentTenantId")
    created_at: Optional[datetime] = Field(None, alias="CreatedAt")
    created_by: Optional[str] = Field(None, alias="CreatedBy")
    modified_at: Optional[datetime] = Field(None, alias="ModifiedAt")
    modified_by: Optional[str] = Field(None, alias="ModifiedBy")
    owner: Optional[str] = Field(None, alias="Owner")
    document_url: Optional[str] = Field(None, alias="DocumentURL")
    feature: Optional[str] = Field(None, alias="Feature")
    category_id: Optional[str] = Field(None, alias="CategoryId")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ListTenantsOutput(BaseModel):
    """Output of list_tenants operation."""

    tenants: List[TenantDetails] = Field(alias="Tenants", default=[])
    next_page_token: Optional[str] = Field(None, alias="NextPageToken")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class GetTenantOutput(TenantDetails):
    """Output of get_tenant operation."""

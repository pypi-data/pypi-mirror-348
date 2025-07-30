"""Tests for the TenantClient class."""

from unittest.mock import MagicMock, patch

import pytest

from day2.models.tenant import GetTenantOutput, ListTenantsOutput
from day2.resources.tenant import TenantClient
from day2.session import Session


@pytest.fixture
def mock_session():
    """Create a mock session for testing."""
    session = MagicMock(spec=Session)
    # Add required attributes for BaseClient
    session._config = MagicMock()
    session._config.api_url = "https://api.example.com"
    session._config.api_version = "v1"
    return session


def test_list_tenants(mock_session):
    """Test listing tenants."""
    # Mock response data
    mock_response = {
        "Tenants": [
            {
                "ID": "tenant-123",
                "Name": "Test Tenant",
                "Owner": "test@example.com",
                "Feature": "FULL",
                "CreatedBy": "admin@example.com",
                "CreatedAt": "2023-01-01T00:00:00Z",
                "ModifiedBy": "admin@example.com",
                "ModifiedAt": "2023-01-01T00:00:00Z",
            }
        ],
        "PageSize": 10,
        "TotalCount": 1,
        "NextPageToken": None,
    }

    # Set up the mock
    with patch.object(
        TenantClient, "_make_request", return_value=mock_response
    ) as mock_make_request:
        # Execute
        client = TenantClient(mock_session)
        result = client.list_tenants(page_size=10)

        # Verify
        mock_make_request.assert_called_once_with(
            "GET", "tenants", params={"PageSize": 10}
        )

    # Verify the result
    assert isinstance(result, ListTenantsOutput)
    assert len(result.tenants) == 1
    assert result.tenants[0].id == "tenant-123"
    assert result.tenants[0].name == "Test Tenant"
    assert result.next_page_token is None


def test_get_tenant(mock_session):
    """Test getting a tenant."""
    # Setup
    tenant_id = "tenant-123"
    mock_response = {
        "ID": "tenant-123",
        "Name": "Test Tenant",
        "Description": "Test description",
        "Owner": "test@example.com",
        "ParentTenantId": None,
        "Feature": "FULL",
        "CategoryId": None,
        "CreatedBy": "admin@example.com",
        "CreatedAt": "2023-01-01T00:00:00Z",
        "ModifiedBy": "admin@example.com",
        "ModifiedAt": "2023-01-01T00:00:00Z",
    }

    # Set up the mock
    with patch.object(
        TenantClient, "_make_request", return_value=mock_response
    ) as mock_make_request:
        # Execute
        client = TenantClient(mock_session)
        result = client.get_tenant(tenant_id)

        # Verify
        mock_make_request.assert_called_once_with("GET", f"tenants/{tenant_id}")

    # Verify the result
    assert isinstance(result, GetTenantOutput)
    assert result.id == "tenant-123"
    assert result.name == "Test Tenant"
    assert result.description == "Test description"

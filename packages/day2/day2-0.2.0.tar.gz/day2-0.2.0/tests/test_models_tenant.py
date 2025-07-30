"""Tests for the tenant models."""

from day2.models.tenant import ListTenantsOutput, TenantDetails


def test_tenant_details_parse():
    """Test parsing a TenantDetails from a dictionary."""
    data = {
        "ID": "tenant-123",
        "Name": "Test Tenant",
        "Description": "Test description",
        "Owner": "test@example.com",
        "Feature": "FULL",
        "CreatedBy": "admin@example.com",
        "CreatedAt": "2023-01-01T00:00:00Z",
        "ModifiedBy": "admin@example.com",
        "ModifiedAt": "2023-01-01T00:00:00Z",
    }

    tenant = TenantDetails.model_validate(data)

    assert tenant.id == "tenant-123"
    assert tenant.name == "Test Tenant"
    assert tenant.description == "Test description"
    assert tenant.owner == "test@example.com"
    assert tenant.feature == "FULL"
    assert tenant.created_by == "admin@example.com"
    assert tenant.modified_by == "admin@example.com"


def test_list_tenants_output_parse():
    """Test parsing a ListTenantsOutput from a dictionary."""
    data = {
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
        "NextPageToken": None,
    }

    list_output = ListTenantsOutput.model_validate(data)

    assert len(list_output.tenants) == 1
    assert list_output.next_page_token is None

    tenant = list_output.tenants[0]
    assert tenant.id == "tenant-123"
    assert tenant.name == "Test Tenant"
    assert tenant.owner == "test@example.com"
    assert tenant.feature == "FULL"


def test_get_tenant_output_parse():
    """Test parsing a GetTenantOutput from a dictionary."""
    data = {
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

    output = TenantDetails.model_validate(data)

    assert output.id == "tenant-123"
    assert output.name == "Test Tenant"
    assert output.description == "Test description"
    assert output.owner == "test@example.com"
    assert output.parent_tenant_id is None
    assert output.feature == "FULL"
    assert output.category_id is None
    assert output.created_by == "admin@example.com"
    assert output.modified_by == "admin@example.com"

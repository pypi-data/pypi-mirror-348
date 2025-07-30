import pytest
from shared_architecture.utils.keycloak_helper import get_user_roles

@pytest.fixture
def valid_token():
    # Mocked Keycloak token structure
    return {
        "preferred_username": "test_user",
        "realm_access": {"roles": ["admin", "user"]}
    }

def test_get_user_roles_returns_roles(valid_token):
    roles = get_user_roles(valid_token)
    assert "admin" in roles
    assert "user" in roles

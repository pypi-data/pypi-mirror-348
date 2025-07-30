from shared_architecture.config.secrets_manager import get_secret


def test_secrets_manager_returns_default_for_missing_key():
    result = get_secret("NON_EXISTENT_SECRET", default="default_value")
    assert result == "default_value"


def test_secrets_manager_returns_env_value(monkeypatch):
    monkeypatch.setenv("TEST_SECRET", "super_secret_value")
    result = get_secret("TEST_SECRET")
    assert result == "super_secret_value"

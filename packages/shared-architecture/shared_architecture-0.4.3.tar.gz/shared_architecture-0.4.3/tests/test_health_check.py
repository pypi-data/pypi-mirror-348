import pytest
from shared_architecture.connection_manager import connection_manager

def aggregate_health_check():
    """
    Aggregates health status from all services using the ConnectionManager.
    """
    return connection_manager.health_check()
def test_aggregate_health_check_returns_expected_keys():
    health_status = aggregate_health_check()
    assert isinstance(health_status, dict)
    assert "redis" in health_status
    assert "timescaledb" in health_status
    assert "rabbitmq" in health_status
    assert "mongodb" in health_status
    assert health_status["redis"] in ["healthy", "unhealthy"]
    assert health_status["timescaledb"] in ["healthy", "unhealthy"]
    assert health_status["rabbitmq"] in ["healthy", "unhealthy"]
    assert health_status["mongodb"] in ["healthy", "unhealthy"]

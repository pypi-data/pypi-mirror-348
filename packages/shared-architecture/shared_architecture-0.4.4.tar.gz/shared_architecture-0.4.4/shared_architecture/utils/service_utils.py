from fastapi import FastAPI
from typing import Optional
from shared_architecture.config.config_manager import ConfigManager
from shared_architecture.utils.logging_utils import configure_logging, log_info, log_error
from shared_architecture.connections import (
    get_redis_connection,
    get_timescaledb_session,
    get_rabbitmq_connection,
    get_mongo_connection,
    close_all_connections
)

def start_service(service_name: str, config_override: Optional[dict] = None) -> FastAPI:
    """
    Centralized service startup: loads config, sets up logging and infrastructure connections.
    Returns a FastAPI app instance.
    """
    # Load config
    config_manager = ConfigManager(service_name=service_name)
    config = config_override or config_manager.config

    # Setup logging
    logger = configure_logging(service_name)
    log_info(f"Starting service '{service_name}' with loaded configuration.")

    # Create FastAPI app
    app = FastAPI(title=config.get("PROJECT_NAME", service_name))
    app.state.settings = config
    app.state.logger = logger

    # Initialize infrastructure connections
    _initialize_infrastructure(app)

    return app


def _initialize_infrastructure(app: FastAPI):
    """
    Connects to all shared infrastructure and sets them on app.state.connections.
    """
    try:
        log_info("Initializing shared infrastructure connections...")

        redis_conn = get_redis_connection()
        timescaledb_conn = get_timescaledb_session()
        rabbitmq_conn = get_rabbitmq_connection()
        mongo_conn = get_mongo_connection()

        app.state.connections = {
            "redis": redis_conn,
            "timescaledb": timescaledb_conn,
            "rabbitmq": rabbitmq_conn,
            "mongo": mongo_conn,
        }

        log_info("All infrastructure connections initialized successfully.")

    except Exception as e:
        log_error(f"Failed to initialize infrastructure: {e}")
        raise


async def stop_service(app: FastAPI):
    """
    Centralized service shutdown: closes all active connections.
    """
    try:
        log_info("Shutting down service...")
        await close_all_connections(app.state.connections)
        log_info("All connections closed gracefully.")
    except Exception as e:
        log_error(f"Error during shutdown: {e}")

from shared_architecture.connections.timescaledb_client import get_timescaledb_session, close_timescaledb_session,timescaledb_client_health_check
from shared_architecture.connections.rabbitmq_client import get_rabbitmq_connection, close_rabbitmq_connection,rabbitmq_client_health_check
from shared_architecture.connections.redis_client import get_redis_connection, close_redis_connection,redis_client_health_check
from shared_architecture.connections.mongodb_client import get_mongo_connection, close_mongo_client,mongo_client_health_check

__all__ = ["ConnectionManager"]

class ConnectionManager:
    def __init__(self):
        self.connections = {
            "timescaledb": None,
            "rabbitmq": None,
            "redis": None,
            "mongodb": None,
        }

    async def initialize_all(self):
        self.connections["timescaledb"] = get_timescaledb_session()
        self.connections["rabbitmq"] = await get_rabbitmq_connection()
        self.connections["redis"] = await get_redis_connection()
        self.connections["mongodb"] = await get_mongo_connection()
        return self.connections

    async def close_all(self):
        if self.connections["timescaledb"]:
            await close_timescaledb_session()
        if self.connections["rabbitmq"]:
            await close_rabbitmq_connection()
        if self.connections["redis"]:
            await close_redis_connection()
        if self.connections["mongodb"]:
            await close_mongo_connection()

    async def health_check(self):
        if self.connections["timescaledb"]:
            await timescaledb_client_health_check()
        if self.connections["rabbitmq"]:
            await rabbitmq_client_health_check()
        if self.connections["redis"]:
            await redis_client_health_check()
        if self.connections["mongodb"]:
            await mongo_client_health_check()
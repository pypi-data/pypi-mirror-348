import os
import sys
import psycopg2
import pika
import redis
from pymongo import MongoClient

def check_timescaledb(url):
    try:
        conn = psycopg2.connect(url)
        conn.close()
        print("✅ TimescaleDB connection successful")
    except Exception as e:
        print(f"❌ TimescaleDB connection failed: {e}")

def check_rabbitmq(url):
    try:
        parameters = pika.URLParameters(url)
        connection = pika.BlockingConnection(parameters)
        connection.close()
        print("✅ RabbitMQ connection successful")
    except Exception as e:
        print(f"❌ RabbitMQ connection failed: {e}")

def check_redis(url):
    try:
        client = redis.Redis.from_url(url)
        client.ping()
        print("✅ Redis connection successful")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")

def check_mongodb(url):
    try:
        client = MongoClient(url, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print("✅ MongoDB connection successful")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")

if __name__ == "__main__":
    check_timescaledb(os.getenv("TIMESCALEDB_URL"))
    check_rabbitmq(os.getenv("RABBITMQ_URL"))
    check_redis(os.getenv("REDIS_URL"))
    check_mongodb(os.getenv("MONGODB_URL"))

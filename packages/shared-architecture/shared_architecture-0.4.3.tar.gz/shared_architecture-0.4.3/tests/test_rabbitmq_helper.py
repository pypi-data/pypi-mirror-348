import pytest
from shared_architecture.utils.rabbitmq_helper import publish_message, declare_queue

@pytest.fixture
def rabbitmq_channel():
    # Stubbed channel or real connection to RabbitMQ should be placed here.
    # You may want to mock this.
    from shared_architecture.connections.rabbitmq_client import get_rabbitmq_channel
    return get_rabbitmq_channel()

def test_declare_queue(rabbitmq_channel):
    queue_name = "test_queue"
    declare_queue(rabbitmq_channel, queue_name)
    # No exception means success

def test_publish_message(rabbitmq_channel):
    queue_name = "test_queue"
    message = "test_message"
    declare_queue(rabbitmq_channel, queue_name)
    publish_message(rabbitmq_channel, queue_name, message)
    # No exception means success
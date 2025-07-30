# tests/test_rabbitmq_mock.py

from shared_architecture.connection_manager import ConnectionManager

def test_publish_message_to_queue():
    cm = ConnectionManager()
    rabbit = cm.get_rabbitmq()
    rabbit.basic_publish(exchange='', routing_key='orders_queue', body='{"order_id": 123}')
    
    assert rabbit.published_messages[-1]["queue"] == "orders_queue"
    assert rabbit.published_messages[-1]["body"] == '{"order_id": 123}'
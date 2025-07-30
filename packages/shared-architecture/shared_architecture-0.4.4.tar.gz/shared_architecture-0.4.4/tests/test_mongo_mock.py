# tests/test_mongo_mock.py

from shared_architecture.connection_manager import ConnectionManager

def test_mongo_find_one_positive():
    cm = ConnectionManager()
    mongo = cm.get_mongo()
    mongo.test_db.test_collection.find_one.return_value = {"user_id": 1}
    
    result = mongo.test_db.test_collection.find_one({"user_id": 1})
    assert result["user_id"] == 1

def test_mongo_find_one_not_found():
    cm = ConnectionManager()
    mongo = cm.get_mongo()
    mongo.test_db.test_collection.find_one.return_value = None
    
    result = mongo.test_db.test_collection.find_one({"user_id": 999})
    assert result is None
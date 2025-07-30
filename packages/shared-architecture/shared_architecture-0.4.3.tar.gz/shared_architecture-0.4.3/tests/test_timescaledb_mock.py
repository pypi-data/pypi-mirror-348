# tests/test_timescaledb_mock.py

from shared_architecture.connection_manager import ConnectionManager
from shared_architecture.db.models.symbol import Symbol

def test_symbol_query_positive():
    cm = ConnectionManager()
    session = cm.get_timescaledb()
    mock_symbol = Symbol(id=1, name="NIFTY", exchange="NSE", instrument_type="EQ")
    session.query.return_value.filter_by.return_value.all.return_value = [mock_symbol]

    results = session.query(Symbol).filter_by(exchange="NSE").all()
    assert len(results) == 1
    assert results[0].name == "NIFTY"

def test_symbol_query_negative():
    cm = ConnectionManager()
    session = cm.get_timescaledb()
    session.query.return_value.filter_by.return_value.all.return_value = []

    results = session.query(Symbol).filter_by(exchange="BSE").all()
    assert results == []
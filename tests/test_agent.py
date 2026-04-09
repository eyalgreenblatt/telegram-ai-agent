from agent import agent_decide

def test_agent_stock():
    result = agent_decide("price AAPL", [])
    assert isinstance(result, str)

def test_agent_chat():
    result = agent_decide("hello bot", [])
    assert isinstance(result, str)

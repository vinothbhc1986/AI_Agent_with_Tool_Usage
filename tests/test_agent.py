import pytest

from agent import SimpleAgent


@pytest.mark.unit
def test_call_agent_returns_advice_for_stress_message():
    agent = SimpleAgent()
    result = agent.call_agent("I'm feeling stressed about work. Any advice?")

    assert "answer" in result
    assert result["used_tool"] == "get_advice"
    assert "advice" in result["answer"].lower()
    assert result["tool_result"]


@pytest.mark.unit
def test_call_agent_returns_book_search_for_book_query():
    agent = SimpleAgent()
    result = agent.call_agent("Find books about machine learning")

    assert "answer" in result
    assert result["used_tool"] == "search_books"
    assert "machine learning" in result["answer"].lower()
    assert result["tool_result"]

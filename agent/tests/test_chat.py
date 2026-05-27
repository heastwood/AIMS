from unittest.mock import MagicMock
from chat import trim_history, send_message


def _make_history(n_messages: int) -> list[dict]:
    """Create n_messages alternating user/assistant messages."""
    roles = ["user", "assistant"]
    return [{"role": roles[i % 2], "content": str(i)} for i in range(n_messages)]


def test_trim_history_drops_oldest_beyond_limit():
    history = _make_history(50)
    result = trim_history(history, max_turns=20)
    assert len(result) == 40
    assert result[0]["content"] == "10"  # first 10 dropped


def test_trim_history_short_history_unchanged():
    history = _make_history(4)
    result = trim_history(history, max_turns=20)
    assert result == history


def test_trim_history_exact_limit_unchanged():
    history = _make_history(40)
    result = trim_history(history, max_turns=20)
    assert len(result) == 40


def test_send_message_returns_response_text():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="AIMS runs on port 443.")]
    )
    result = send_message(mock_client, "What port does AIMS use?", [], "knowledge")
    assert result == "AIMS runs on port 443."


def test_send_message_appends_user_message_to_history():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="OK")]
    )
    history = [
        {"role": "user", "content": "previous question"},
        {"role": "assistant", "content": "previous answer"},
    ]
    send_message(mock_client, "new question", history, "kb")
    call_kwargs = mock_client.messages.create.call_args.kwargs
    messages = call_kwargs["messages"]
    assert messages[-1] == {"role": "user", "content": "new question"}
    assert messages[0]["content"] == "previous question"


def test_send_message_uses_correct_model():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="OK")]
    )
    send_message(mock_client, "hi", [], "kb")
    call_kwargs = mock_client.messages.create.call_args.kwargs
    assert call_kwargs["model"] == "claude-sonnet-4-6"


def test_send_message_applies_cache_control_to_system():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="OK")]
    )
    send_message(mock_client, "hi", [], "kb content")
    call_kwargs = mock_client.messages.create.call_args.kwargs
    system = call_kwargs["system"]
    assert isinstance(system, list)
    assert system[0]["cache_control"] == {"type": "ephemeral"}

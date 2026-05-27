import anthropic

SYSTEM_PROMPT_TEMPLATE = """\
You are an AIMS implementation and troubleshooting specialist at Quadient. \
You assist with AIMS500 and AIMS1000 installations, Impress Automate integration, \
third-party OMS integration (Ricoh Process Director, Pitney Bowes MRDF), \
Active Directory user/group setup, Windows service account configuration, \
firewall and network port requirements, and JAF/JCF/JRF file formats.

Answer questions clearly and concisely. If a question falls outside AIMS knowledge, say so.

# AIMS Knowledge Base

{knowledge}"""

MAX_HISTORY_TURNS = 20


def build_system_prompt(knowledge: str) -> str:
    return SYSTEM_PROMPT_TEMPLATE.format(knowledge=knowledge)


def trim_history(history: list[dict], max_turns: int = MAX_HISTORY_TURNS) -> list[dict]:
    """Keep only the last max_turns pairs (user + assistant) from history."""
    max_messages = max_turns * 2
    if len(history) > max_messages:
        return history[-max_messages:]
    return history


def send_message(
    client: anthropic.Anthropic,
    user_message: str,
    history: list[dict],
    knowledge: str,
) -> str:
    """Send a user message to Claude and return the assistant's response text."""
    system = [
        {
            "type": "text",
            "text": build_system_prompt(knowledge),
            "cache_control": {"type": "ephemeral"},
        }
    ]

    messages = trim_history(history) + [{"role": "user", "content": user_message}]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=system,
        messages=messages,
    )

    return response.content[0].text

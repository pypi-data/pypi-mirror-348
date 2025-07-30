"""
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""

from typing import Any, Dict

from teams_memory.interfaces.types import (
    AssistantMessage,
    InternalMessage,
    Message,
    UserMessage,
)


def build_message_from_dict(row: Dict[str, Any]) -> Message:
    """Build a message object from a dictionary which contains the message data."""

    if row["type"] == "internal":
        return InternalMessage(**row)
    elif row["type"] == "user":
        return UserMessage(**row)
    elif row["type"] == "assistant":
        return AssistantMessage(**row)
    else:
        raise ValueError(
            f"Invalid message type: {row['type']}. Expected one of: 'internal', 'user', 'assistant'"
        )

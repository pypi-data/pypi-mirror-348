"""Signal related classes/enums."""

from enum import Enum


class Signal(str, Enum):
    """Available signal prefixes."""

    PROGRESS = "progress"
    OUTPUTS = "outputs"
    TOOL_COMMAND = "tool_command"
    ERROR_MESSAGE = "error_message"


def get_signal_id(id: str, signal: Signal) -> str:
    return f"{id}_{signal}"


class ToolCommand(str, Enum):
    """Available commands for tools."""

    STOP = "stop"
    START = "start"
    CANCEL = "cancel"
    GET_RESULTS = "get_results"

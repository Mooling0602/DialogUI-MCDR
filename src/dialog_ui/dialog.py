from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal


class DialogType(Enum):
    """Dialog types from the `minecraft:dialog_type` registry."""

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        """This method add a string "minecraft:" as namespace prefix to each types."""
        _start = start
        _count = count
        _last_values = last_values
        return f"minecraft:{name.lower()}"

    CONFIRMATION = auto()
    """A dialog screen with yes and no action buttons in footer."""

    DIALOG_LIST = auto()
    """A dialog screen with scrollable list of buttons leading directly to other dialogs."""

    MULTI_ACTION = auto()
    """A dialog screen with a scrollable list of action buttons."""

    NOTICE = auto()
    """A dialog screen with a single action button in footer."""

    SERVER_LINKS = auto()
    """A dialog screen with scrollable list of server links."""


class DialogAfterActionOperation(Enum):
    """Possible operations will be performed on the dialog after click or submit actions."""

    CLOSE = "close"
    """Closes the dialog and returns to the previous non-dialog screen (if any)."""

    NONE = "none"
    """Does nothing, i.e. keeps the current dialog screen open (only available if "pause" is `false` to avoid locking the game in single-player mode)."""

    WAIT_FOR_RESPONSE = "wait_for_response"
    """Replace the current dialog with a "Waiting for Response" screen."""


@dataclass
class DialogBase:
    """An base class of Minecraft dialog component."""

    body: list[dict] | dict  # should impl component
    """Optional list of body elements or a single body element."""

    input: list[dict]  # should impl component
    """Optional list of input controls."""

    after_action: DialogAfterActionOperation = DialogAfterActionOperation.CLOSE
    """An additional operation performed on the dialog after click or submit actions. Defaults to `close`."""

    can_close_with_escape: bool = True
    """Can dialog be dismissed with Escape key. Defaults to `true`."""


if __name__ == "__main__":
    print(type(DialogBase.after_action))
    print(DialogBase.after_action)
    print(DialogBase)

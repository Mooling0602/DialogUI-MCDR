from dataclasses import dataclass
from enum import Enum, auto

from mcdreforged.api.all import RText


class DialogType(Enum):
    """Dialog types from the `minecraft:dialog_type` registry.
    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        """This method add a string "minecraft:" as namespace prefix to each types."""
        _start = start
        _count = count
        _last_values = last_values
        return f"minecraft:{name.lower()}"

    CONFIRMATION = auto()
    """A dialog screen with yes and no action buttons in footer.
    `Ref: <https://minecraft.wiki/w/Dialog#confirmation>`__"""

    DIALOG_LIST = auto()
    """A dialog screen with scrollable list of buttons leading directly to other dialogs.
    `Ref: <https://minecraft.wiki/w/Dialog#dialog_list>`__"""

    MULTI_ACTION = auto()
    """A dialog screen with a scrollable list of action buttons.
    `Ref: <https://minecraft.wiki/w/Dialog#multi_action>`__"""

    NOTICE = auto()
    """A dialog screen with a single action button in footer.
    `Ref: <https://minecraft.wiki/w/Dialog#notice>`__"""

    SERVER_LINKS = auto()
    """A dialog screen with scrollable list of server links.
    `Ref: <https://minecraft.wiki/w/Dialog#server_links>`__"""


class DialogAfterActionOperation(Enum):
    """Possible operations will be performed on the dialog after click or submit actions.
    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    CLOSE = "close"
    """Closes the dialog and returns to the previous non-dialog screen (if any).
    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    NONE = "none"
    """Does nothing, i.e. keeps the current dialog screen open (only available if "pause" is `false` to avoid locking the game in single-player mode).
    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    WAIT_FOR_RESPONSE = "wait_for_response"
    """Replace the current dialog with a "Waiting for Response" screen.
    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""


@dataclass
class DialogBase:
    """An base class of Minecraft dialog component.
    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    title: RText
    """The title text component of the dialog.
    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    external_title: RText | None = None
    """Name to be used for a button leading to this dialog (e.g. on the pause menu or in a parent ``dialog_list``), optional text component.
    If not present, ``title`` is used instead.
    `Ref: <https://minecraft.wiki/w/Dialog#dialog_list>`__"""

    pause: bool = True
    """If the dialog screen should pause the game in single-player mode. Defaults to ``true``.
    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    after_action: DialogAfterActionOperation = DialogAfterActionOperation.CLOSE
    """An additional operation performed on the dialog after click or submit actions. Defaults to ``close``.
    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    can_close_with_escape: bool = True
    """Can dialog be dismissed with Escape key. Defaults to ``true``.
    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""


if __name__ == "__main__":
    print(type(DialogBase.after_action))
    print(DialogBase.after_action)
    print(DialogBase)

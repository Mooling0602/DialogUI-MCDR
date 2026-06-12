"""Enum types and helpers for Minecraft dialog component formats.

`Ref: <https://minecraft.wiki/w/Dialog>`__
"""

from enum import Enum, auto

_minecraft_namespace = "minecraft:"


def check_if_type_matched(value: str, expected: str) -> bool:
    if not expected.startswith(_minecraft_namespace):
        raise ValueError("Expected should be a 'minecraft:' prefixed string.")
    return value == expected or f"{_minecraft_namespace}{value}" == expected


class DialogType(Enum):
    """Dialog types from the `minecraft:dialog_type` registry.
    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        """This method add a string "minecraft:" as namespace prefix to each types."""
        _, _, _ = start, count, last_values
        return _minecraft_namespace + name.lower()

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


class DialogActionType(Enum):
    """Static action types used by dialog buttons.

    `Ref: <https://minecraft.wiki/w/Dialog#Static_action_types>`__
    """

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        """This method add a string "minecraft:" as namespace prefix to each types."""
        _, _, _ = start, count, last_values
        return f"minecraft:{name.lower()}"

    SHOW_DIALOG = auto()
    """Open a dialog by ID or inline definition.
    `Ref: <https://minecraft.wiki/w/Dialog#show_dialog>`__"""

    OPEN_URL = auto()
    """Open a URL in the user's default web browser.
    `Ref: <https://minecraft.wiki/w/Dialog#open_url>`__"""

    RUN_COMMAND = auto()
    """Run a command as if typed by the player.
    `Ref: <https://minecraft.wiki/w/Dialog#run_command>`__"""

    SUGGEST_COMMAND = auto()
    """Open chat and fill it with text or a command.
    `Ref: <https://minecraft.wiki/w/Dialog#suggest_command>`__"""

    CHANGE_PAGE = auto()
    """Change to a page in contexts that support page navigation.
    `Ref: <https://minecraft.wiki/w/Dialog#change_page>`__"""

    COPY_TO_CLIPBOARD = auto()
    """Copy text to the user's clipboard.
    `Ref: <https://minecraft.wiki/w/Dialog#copy_to_clipboard>`__"""

    CUSTOM = auto()
    """Send a custom event to the server.
    `Ref: <https://minecraft.wiki/w/Dialog#custom>`__"""


class DialogActionTypeDynamic(Enum):
    """Dynamic action types that use submitted input values.

    `Ref: <https://minecraft.wiki/w/Dialog#Dynamic_action_types>`__
    """

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        _, _, _ = start, count, last_values
        return f"minecraft:dynamic/{name.lower()}"

    RUN_COMMAND = auto()
    """Build a run-command event from a macro template.
    `Ref: <https://minecraft.wiki/w/Dialog#dynamic/run_command>`__"""

    CUSTOM = auto()
    """Build a custom event carrying all submitted input values.
    `Ref: <https://minecraft.wiki/w/Dialog#dynamic/custom>`__"""


class DialogBodyType(Enum):
    """Body element types from the ``minecraft:dialog_body_type`` registry.

    `Ref: <https://minecraft.wiki/w/Dialog#Body_format>`__
    """

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        _, _, _ = start, count, last_values
        return f"minecraft:{name.lower()}"

    PLAIN_MESSAGE = auto()
    """A multiline label.
    `Ref: <https://minecraft.wiki/w/Dialog#plain_message>`__"""

    ITEM = auto()
    """An item stack with optional description.
    `Ref: <https://minecraft.wiki/w/Dialog#item>`__"""


class DialogInputsType(Enum):
    """Input control types from the ``minecraft:input_control_type`` registry.

    `Ref: <https://minecraft.wiki/w/Dialog#Input_control_format>`__
    """

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        _, _, _ = start, count, last_values
        return f"minecraft:{name.lower()}"

    TEXT = auto()
    """A text input field.
    `Ref: <https://minecraft.wiki/w/Dialog#text>`__"""

    BOOLEAN = auto()
    """A checkbox input.
    `Ref: <https://minecraft.wiki/w/Dialog#boolean>`__"""

    SINGLE_OPTION = auto()
    """A preset option selector.
    `Ref: <https://minecraft.wiki/w/Dialog#single_option>`__"""

    NUMBER_RANGE = auto()
    """A number slider.
    `Ref: <https://minecraft.wiki/w/Dialog#number_range>`__"""


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

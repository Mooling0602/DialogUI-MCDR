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
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        """This method add a string "minecraft:" as namespace prefix to each types."""
        _, _, _ = start, count, last_values
        return f"minecraft:{name.lower()}"

    SHOW_DIALOG = auto()
    OPEN_URL = auto()
    RUN_COMMAND = auto()
    SUGGEST_COMMAND = auto()
    CHANGE_PAGE = auto()
    COPY_TO_CLIPBOARD = auto()
    CUSTOM = auto()


class DialogActionTypeDynamic(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        _, _, _ = start, count, last_values
        return f"minecraft:dynamic/{name.lower()}"

    RUN_COMMAND = auto()
    CUSTOM = auto()


class DialogBodyType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        _, _, _ = start, count, last_values
        return f"minecraft:{name.lower()}"

    PLAIN_MESSAGE = auto()
    ITEM = auto()


class DialogInputsType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        _, _, _ = start, count, last_values
        return f"minecraft:{name.lower()}"

    TEXT = auto()
    BOOLEAN = auto()
    SINGLE_OPTION = auto()
    NUMBER_RANGE = auto()


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

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Self

from mcdreforged.api.all import RText, RTextBase


class DialogType(Enum):
    """Dialog types from the `minecraft:dialog_type` registry.
    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        """This method add a string "minecraft:" as namespace prefix to each types."""
        _, _, _ = start, count, last_values
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

    .. warning::
       Do not use `dataclass.asdict()` to convert this class to a dict, as it will not convert the correct data structure for the dialog component.
       Instead, use the `to_dict()` method provided in this class.

    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    type: DialogType
    """One dialog types from the `minecraft:dialog_type` registry.
    """

    title: RTextBase
    """The title text component of the dialog.
    """

    can_close_with_escape: bool = True
    """Can dialog be dismissed with Escape key. Defaults to ``true``.
    """

    pause: bool = True
    """If the dialog screen should pause the game in single-player mode. Defaults to ``true``.
    """

    after_action: DialogAfterActionOperation = DialogAfterActionOperation.CLOSE
    """An additional operation performed on the dialog after click or submit actions. Defaults to ``close``.
    """

    external_title: RTextBase | None = None
    """Name to be used for a button leading to this dialog (e.g. on the pause menu or in a parent ``dialog_list``), optional text component.
    If not present, ``title`` is used instead.
    """

    body: list | None = None  # need impl class
    """Optional list of body elements or a single body element.
    `Ref: <https://minecraft.wiki/w/Dialog#Body_format>`__"""

    inputs: list | None = None  # need impl class
    """Optional list of input controls.
    `Ref: <https://minecraft.wiki/w/Dialog#Input_control_format>`__"""

    def to_dict(self) -> dict:
        """Convert the dataclass to a dict with correct data structure for the dialog component."""
        return {
            "type": self.type.value,
            "title": self.title.to_json_object(),
            "external_title": self.external_title.to_json_object()
            if self.external_title is not None
            else None,
            "body": [element.to_dict() for element in self.body] if self.body else None,
            "inputs": [input_control.to_dict() for input_control in self.inputs]
            if self.inputs
            else None,
            "can_close_with_escape": self.can_close_with_escape,
            "pause": self.pause,
            "after_action": self.after_action.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        type = DialogType(data["type"])
        after_action_option = data.get("after_action", "close")
        after_action = DialogAfterActionOperation(after_action_option)
        title = RTextBase.from_json_object(data["title"])
        external_title = None
        if data.get("external_title", None):
            external_title = RTextBase.from_json_object(data["external_title"])
        body = None
        if data.get("body", None):
            body = data["body"]  # need impl body element class and methods.
        inputs = None
        if data.get("inputs", None):
            inputs = data["inputs"]  # need impl input control class and methods.
        return cls(
            type=type,
            title=title,
            can_close_with_escape=data.get("can_close_with_escape", True),
            pause=data.get("pause", True),
            after_action=after_action,
            external_title=external_title,
            body=body,
            inputs=inputs,
        )


@dataclass
class DialogActionBase:
    type: DialogActionType | DialogActionTypeDynamic


class DialogActionShowDialog(DialogActionBase):
    type: DialogActionType = field(init=False, default=DialogActionType.SHOW_DIALOG)
    dialog: str | DialogBase

    def __post_init__(self):
        self.type = DialogActionType.SHOW_DIALOG


class DialogActionOpenUrl(DialogActionBase):
    type: DialogActionType = field(init=False, default=DialogActionType.OPEN_URL)
    url: str

    def __post_init__(self):
        self.type = DialogActionType.OPEN_URL


class DialogActionRunCommand(DialogActionBase):
    type: DialogActionType = field(init=False, default=DialogActionType.RUN_COMMAND)
    command: str

    def __post_init__(self):
        self.type = DialogActionType.RUN_COMMAND


class DialogActionSuggestCommand(DialogActionBase):
    type: DialogActionType = field(init=False, default=DialogActionType.SUGGEST_COMMAND)
    command: str

    def __post_init__(self):
        self.type = DialogActionType.SUGGEST_COMMAND


class DialogActionChangePage(DialogActionBase):
    type: DialogActionType = field(init=False, default=DialogActionType.CHANGE_PAGE)
    page: int

    def __post_init__(self):
        self.type = DialogActionType.CHANGE_PAGE


class DialogActionCopyToClipboard(DialogActionBase):
    type: DialogActionType = field(init=False, default=DialogActionType.COPY_TO_CLIPBOARD)
    value: str

    def __post_init__(self):
        self.type = DialogActionType.COPY_TO_CLIPBOARD


class DialogActionCustom(DialogActionBase):
    type: DialogActionType = field(init=False, default=DialogActionType.CUSTOM)
    id: str
    payload: str | Any

    def __post_init__(self):
        self.type = DialogActionType.CUSTOM


class DialogActionRunCommandDynamic(DialogActionBase):
    type: DialogActionTypeDynamic = field(init=False, default=DialogActionTypeDynamic.RUN_COMMAND)
    template: str

    def __post_init__(self):
        self.type = DialogActionTypeDynamic.RUN_COMMAND


@dataclass
class DialogActionCustomDynamic(DialogActionBase):
    type: DialogActionTypeDynamic = field(init=False, default=DialogActionTypeDynamic.CUSTOM)
    additions: dict
    id: str

    def __post_init__(self):
        self.type = DialogActionTypeDynamic.CUSTOM


@dataclass
class DialogAction:
    label: RTextBase
    action: DialogActionBase


@dataclass
class DialogNoticeAction:
    label: RTextBase = field(default_factory=lambda: RText("gui.ok"))
    tooltip: RTextBase | None = None
    width: int = 150
    action: DialogAction | None = None


@dataclass
class DialogNotice(DialogBase):
    type: DialogType = field(init=False, default=DialogType.NOTICE)
    action: DialogNoticeAction | None = None

    def __post_init__(self):
        self.type = DialogType.NOTICE


if __name__ == "__main__":
    pass  # impl test logic here.

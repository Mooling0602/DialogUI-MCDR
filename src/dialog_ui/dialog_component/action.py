"""Dialog action classes matching Minecraft dialog action format.

`Ref: <https://minecraft.wiki/w/Dialog#Action_format>`__
"""

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Self

from mcdreforged.api.all import RTextBase

from dialog_ui.dialog_component.base import DialogBase
from dialog_ui.dialog_component.types import (
    DialogActionType,
    DialogActionTypeDynamic,
    check_if_type_matched,
)


@dataclass
class DialogActionBase:
    """Base class for static or dynamic dialog action payloads.

    `Ref: <https://minecraft.wiki/w/Dialog#Action_format>`__
    """

    @property
    @abstractmethod
    def type(self) -> DialogActionType | DialogActionTypeDynamic:
        """One action type from the static or dynamic action registries."""
        ...

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError(
            "DialogActionBase does not support serialization, please use the specific dialog action class instead."
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DialogActionBase":
        _action_type_dispatch: dict[str, type[DialogActionBase]] = {
            DialogActionType.SHOW_DIALOG.value: DialogActionShowDialog,
            DialogActionType.OPEN_URL.value: DialogActionOpenUrl,
            DialogActionType.RUN_COMMAND.value: DialogActionRunCommand,
            DialogActionType.SUGGEST_COMMAND.value: DialogActionSuggestCommand,
            DialogActionType.CHANGE_PAGE.value: DialogActionChangePage,
            DialogActionType.COPY_TO_CLIPBOARD.value: DialogActionCopyToClipboard,
            DialogActionType.CUSTOM.value: DialogActionCustom,
            DialogActionTypeDynamic.RUN_COMMAND.value: DialogActionRunCommandDynamic,
            DialogActionTypeDynamic.CUSTOM.value: DialogActionCustomDynamic,
        }
        action_type = data.get("type", "")
        action_cls = _action_type_dispatch.get(action_type)
        if action_cls is None:
            raise ValueError(f"Unknown action type: {action_type}")
        return action_cls.from_dict(data)


@dataclass
class DialogActionShowDialog(DialogActionBase):
    """Open another dialog by resource location or inline definition.

    `Ref: <https://minecraft.wiki/w/Dialog#show_dialog>`__
    """

    _type: DialogActionType = field(init=False, default=DialogActionType.SHOW_DIALOG)
    dialog: str | DialogBase
    """Dialog resource location or inline dialog object to display."""

    @property
    def type(self) -> DialogActionType:
        return self._type

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "dialog": self.dialog.to_dict()
            if isinstance(self.dialog, DialogBase)
            else self.dialog,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(
            _type, DialogActionType.SHOW_DIALOG.value
        ):
            raise ValueError("Invalid type for DialogActionShowDialog")
        dialog_data = data["dialog"]
        if isinstance(dialog_data, dict):
            dialog_data = DialogBase.from_dict(dialog_data)
        return cls(dialog=dialog_data)


@dataclass
class DialogActionOpenUrl(DialogActionBase):
    """Open a URL in the user's default web browser.

    `Ref: <https://minecraft.wiki/w/Dialog#open_url>`__
    """

    _type: DialogActionType = field(init=False, default=DialogActionType.OPEN_URL)
    url: str
    """The URL to open."""

    @property
    def type(self) -> DialogActionType:
        return self._type

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "url": self.url,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(
            _type, DialogActionType.OPEN_URL.value
        ):
            raise ValueError("Invalid type for DialogActionOpenUrl")
        return cls(url=data["url"])


@dataclass
class DialogActionRunCommand(DialogActionBase):
    """Run a command as if the player typed it in chat.

    `Ref: <https://minecraft.wiki/w/Dialog#run_command>`__
    """

    _type: DialogActionType = field(init=False, default=DialogActionType.RUN_COMMAND)
    command: str
    """Command to run, usually without a leading slash."""

    @property
    def type(self) -> DialogActionType:
        return self._type

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "command": self.command,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(
            _type, DialogActionType.RUN_COMMAND.value
        ):
            raise ValueError("Invalid type for DialogActionRunCommand")
        return cls(command=data["command"])


@dataclass
class DialogActionSuggestCommand(DialogActionBase):
    """Open chat and fill it with the given text or command.

    `Ref: <https://minecraft.wiki/w/Dialog#suggest_command>`__
    """

    _type: DialogActionType = field(
        init=False, default=DialogActionType.SUGGEST_COMMAND
    )
    command: str
    """Text or command inserted into the chat input."""

    @property
    def type(self) -> DialogActionType:
        return self._type

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "command": self.command,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(
            _type, DialogActionType.SUGGEST_COMMAND.value
        ):
            raise ValueError("Invalid type for DialogActionSuggestCommand")
        return cls(command=data["command"])


@dataclass
class DialogActionChangePage(DialogActionBase):
    """Change to a page in contexts that support page navigation.

    `Ref: <https://minecraft.wiki/w/Dialog#change_page>`__
    """

    _type: DialogActionType = field(init=False, default=DialogActionType.CHANGE_PAGE)
    page: int
    """Target page number."""

    @property
    def type(self) -> DialogActionType:
        return self._type

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "page": self.page,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(
            _type, DialogActionType.CHANGE_PAGE.value
        ):
            raise ValueError("Invalid type for DialogActionChangePage")
        return cls(page=data["page"])


@dataclass
class DialogActionCopyToClipboard(DialogActionBase):
    """Copy text to the user's clipboard.

    `Ref: <https://minecraft.wiki/w/Dialog#copy_to_clipboard>`__
    """

    _type: DialogActionType = field(
        init=False, default=DialogActionType.COPY_TO_CLIPBOARD
    )
    value: str
    """Text to copy."""

    @property
    def type(self) -> DialogActionType:
        return self._type

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "value": self.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(
            _type, DialogActionType.COPY_TO_CLIPBOARD.value
        ):
            raise ValueError("Invalid type for DialogActionCopyToClipboard")
        return cls(value=data["value"])


@dataclass
class DialogActionCustom(DialogActionBase):
    """Send a custom event to the server.

    `Ref: <https://minecraft.wiki/w/Dialog#custom>`__
    """

    _type: DialogActionType = field(init=False, default=DialogActionType.CUSTOM)
    id: str
    """Namespaced identifier for the custom event."""

    payload: str | Any
    """Optional event payload."""

    @property
    def type(self) -> DialogActionType:
        return self._type

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "id": self.id,
            "payload": self.payload,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(_type, DialogActionType.CUSTOM.value):
            raise ValueError("Invalid type for DialogActionCustom")
        return cls(
            id=data["id"],
            payload=data["payload"],
        )


@dataclass
class DialogActionRunCommandDynamic(DialogActionBase):
    """Build a run-command action using submitted input values.

    `Ref: <https://minecraft.wiki/w/Dialog#dynamic/run_command>`__
    """

    _type: DialogActionTypeDynamic = field(
        init=False, default=DialogActionTypeDynamic.RUN_COMMAND
    )
    template: str
    """Macro template interpreted as a command."""

    @property
    def type(self) -> DialogActionTypeDynamic:
        return self._type

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "template": self.template,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(
            _type, DialogActionTypeDynamic.RUN_COMMAND.value
        ):
            raise ValueError("Invalid type for DialogActionRunCommandDynamic")
        return cls(template=data["template"])


@dataclass
class DialogActionCustomDynamic(DialogActionBase):
    """Build a custom event from submitted input values.

    `Ref: <https://minecraft.wiki/w/Dialog#dynamic/custom>`__
    """

    _type: DialogActionTypeDynamic = field(
        init=False, default=DialogActionTypeDynamic.CUSTOM
    )
    additions: dict
    """Static fields added to the generated payload."""

    id: str
    """Namespaced identifier for the generated custom event."""

    @property
    def type(self) -> DialogActionTypeDynamic:
        return self._type

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "additions": self.additions,
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(
            _type, DialogActionTypeDynamic.CUSTOM.value
        ):
            raise ValueError("Invalid type for DialogActionCustomDynamic")
        return cls(
            additions=data["additions"],
            id=data["id"],
        )


@dataclass
class DialogAction:
    """Labeled button action used by dialog footer and list buttons.

    `Ref: <https://minecraft.wiki/w/Dialog#Action_format>`__
    """

    label: RTextBase
    """Button label text component."""

    action: DialogActionBase
    """Action payload performed when the button is clicked."""

    def to_dict(self) -> dict:
        return {
            "label": self.label.to_json_object(),
            "action": self.action.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            label=RTextBase.from_json_object(data["label"]),
            action=DialogActionBase.from_dict(data["action"]),
        )

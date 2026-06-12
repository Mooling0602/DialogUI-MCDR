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
    @property
    @abstractmethod
    def type(self) -> DialogActionType | DialogActionTypeDynamic: ...

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
    _type: DialogActionType = field(init=False, default=DialogActionType.SHOW_DIALOG)
    dialog: str | DialogBase

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
    _type: DialogActionType = field(init=False, default=DialogActionType.OPEN_URL)
    url: str

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
    _type: DialogActionType = field(init=False, default=DialogActionType.RUN_COMMAND)
    command: str

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
    _type: DialogActionType = field(
        init=False, default=DialogActionType.SUGGEST_COMMAND
    )
    command: str

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
    _type: DialogActionType = field(init=False, default=DialogActionType.CHANGE_PAGE)
    page: int

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
    _type: DialogActionType = field(
        init=False, default=DialogActionType.COPY_TO_CLIPBOARD
    )
    value: str

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
    _type: DialogActionType = field(init=False, default=DialogActionType.CUSTOM)
    id: str
    payload: str | Any

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
    _type: DialogActionTypeDynamic = field(
        init=False, default=DialogActionTypeDynamic.RUN_COMMAND
    )
    template: str

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
    _type: DialogActionTypeDynamic = field(
        init=False, default=DialogActionTypeDynamic.CUSTOM
    )
    additions: dict
    id: str

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
    label: RTextBase
    action: DialogActionBase

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

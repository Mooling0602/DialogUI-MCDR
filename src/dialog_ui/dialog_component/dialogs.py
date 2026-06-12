"""Concrete dialog classes: DialogNotice, DialogConfirmation, DialogMultiAction, DialogServerLinks, DialogList."""

from dataclasses import dataclass, field
from typing import Any, Self

from mcdreforged.api.all import RText

from dialog_ui.dialog_component.base import DialogBase, DialogNoticeAction
from dialog_ui.dialog_component.types import (
    DialogType,
    check_if_type_matched,
)


@dataclass
class DialogNotice(DialogBase):
    _type: DialogType = field(init=False, default=DialogType.NOTICE)
    action: DialogNoticeAction | None = None

    @property
    def type(self) -> DialogType:
        return self._type

    def to_dict(self) -> dict:
        result: dict[str, Any] = super().to_dict()
        if self.action:
            result.update({"action": self.action.to_dict()})
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(_type, DialogType.NOTICE.value):
            raise ValueError("Invalid type for DialogNotice")
        kwargs = cls._parse_base_kwargs(data)
        kwargs["action"] = (
            DialogNoticeAction.from_dict(data["action"]) if "action" in data else None
        )
        return cls(**kwargs)


@dataclass
class DialogConfirmation(DialogBase):
    _type: DialogType = field(init=False, default=DialogType.CONFIRMATION)

    @property
    def type(self) -> DialogType:
        return self._type

    yes: DialogNoticeAction = field(
        default_factory=lambda: DialogNoticeAction(label=RText("Yes"))
    )
    no: DialogNoticeAction = field(
        default_factory=lambda: DialogNoticeAction(label=RText("No"))
    )

    def to_dict(self) -> dict:
        result: dict[str, Any] = super().to_dict()
        result.update(
            {
                "yes": self.yes.to_dict(),
                "no": self.no.to_dict(),
            }
        )
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(_type, DialogType.CONFIRMATION.value):
            raise ValueError("Invalid type for DialogConfirmation")
        kwargs = cls._parse_base_kwargs(data)
        kwargs["yes"] = DialogNoticeAction.from_dict(data["yes"])
        kwargs["no"] = DialogNoticeAction.from_dict(data["no"])
        return cls(**kwargs)


@dataclass
class DialogMultiAction(DialogBase):
    _type: DialogType = field(init=False, default=DialogType.MULTI_ACTION)

    @property
    def type(self) -> DialogType:
        return self._type

    actions: list[DialogNoticeAction] = field(default_factory=list)
    columns: int | None = None
    exit_action: DialogNoticeAction | None = None

    def to_dict(self) -> dict:
        result: dict[str, Any] = super().to_dict()
        result.update(
            {
                "actions": [action.to_dict() for action in self.actions],
            }
        )
        if self.columns is not None:
            result.update({"columns": self.columns})
        if self.exit_action:
            result.update({"exit_action": self.exit_action.to_dict()})
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(_type, DialogType.MULTI_ACTION.value):
            raise ValueError("Invalid type for DialogMultiAction")
        kwargs = cls._parse_base_kwargs(data)
        kwargs["actions"] = [
            DialogNoticeAction.from_dict(action) for action in data["actions"]
        ]
        kwargs["columns"] = data.get("columns", None)
        kwargs["exit_action"] = (
            DialogNoticeAction.from_dict(data["exit_action"])
            if "exit_action" in data
            else None
        )
        return cls(**kwargs)


@dataclass
class DialogServerLinks(DialogBase):
    _type: DialogType = field(init=False, default=DialogType.SERVER_LINKS)

    @property
    def type(self) -> DialogType:
        return self._type

    exit_action: DialogNoticeAction | None = None
    columns: int | None = None
    button_width: int | None = None

    def to_dict(self) -> dict:
        result: dict[str, Any] = super().to_dict()
        if self.exit_action:
            result.update({"exit_action": self.exit_action.to_dict()})
        if self.columns is not None:
            result.update({"columns": self.columns})
        if self.button_width is not None:
            result.update({"button_width": self.button_width})
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(_type, DialogType.SERVER_LINKS.value):
            raise ValueError("Invalid type for DialogServerLinks")
        kwargs = cls._parse_base_kwargs(data)
        kwargs["exit_action"] = (
            DialogNoticeAction.from_dict(data["exit_action"])
            if "exit_action" in data
            else None
        )
        kwargs["columns"] = data.get("columns", None)
        kwargs["button_width"] = data.get("button_width", None)
        return cls(**kwargs)


@dataclass
class DialogList(DialogBase):
    _type: DialogType = field(init=False, default=DialogType.DIALOG_LIST)

    @property
    def type(self) -> DialogType:
        return self._type

    dialogs: str | list[DialogBase | str] | DialogBase = field(kw_only=True)
    exit_action: DialogNoticeAction | None = None
    columns: int | None = None
    button_width: int | None = None

    def to_dict(self) -> dict:
        result: dict[str, Any] = super().to_dict()
        if isinstance(self.dialogs, str):
            result.update({"dialogs": self.dialogs})
        elif isinstance(self.dialogs, list):
            result.update(
                {
                    "dialogs": [
                        dialog.to_dict() if isinstance(dialog, DialogBase) else dialog
                        for dialog in self.dialogs
                    ]
                }
            )
        elif isinstance(self.dialogs, DialogBase):
            result.update({"dialogs": self.dialogs.to_dict()})
        if self.exit_action:
            result.update({"exit_action": self.exit_action.to_dict()})
        if self.columns is not None:
            result.update({"columns": self.columns})
        if self.button_width is not None:
            result.update({"button_width": self.button_width})
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(_type, DialogType.DIALOG_LIST.value):
            raise ValueError("Invalid type for DialogList")

        dialogs_data = data["dialogs"]
        dialogs: str | list[DialogBase | str] | DialogBase
        if isinstance(dialogs_data, str):
            dialogs = dialogs_data
        elif isinstance(dialogs_data, list):
            dialogs = [
                DialogBase.from_dict(item) if isinstance(item, dict) else item
                for item in dialogs_data
            ]
        elif isinstance(dialogs_data, dict):
            dialogs = DialogBase.from_dict(dialogs_data)
        else:
            dialogs = dialogs_data

        kwargs = cls._parse_base_kwargs(data)
        kwargs["dialogs"] = dialogs
        kwargs["exit_action"] = (
            DialogNoticeAction.from_dict(data["exit_action"])
            if "exit_action" in data
            else None
        )
        kwargs["columns"] = data.get("columns", None)
        kwargs["button_width"] = data.get("button_width", None)
        return cls(**kwargs)

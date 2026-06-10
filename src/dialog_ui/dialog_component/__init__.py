"""Dialog component module - provides easy access to all dialog-related classes."""

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Self, cast

from mcdreforged.api.all import RText, RTextBase

from dialog_ui.dialog_component.action import (
    DialogAction,
    DialogActionBase,
    DialogActionChangePage,
    DialogActionCopyToClipboard,
    DialogActionCustom,
    DialogActionCustomDynamic,
    DialogActionOpenUrl,
    DialogActionRunCommand,
    DialogActionRunCommandDynamic,
    DialogActionShowDialog,
    DialogActionSuggestCommand,
)
from dialog_ui.dialog_component.body import (
    DialogBodyBase,
    DialogBodyItem,
    DialogBodyItemDescription,
    DialogBodyItemObject,
    DialogBodyPlainMessage,
)
from dialog_ui.dialog_component.inputs import (
    DialogInputsBase,
    DialogInputsBoolean,
    DialogInputsNumberRange,
    DialogInputsSingleOption,
    DialogInputsSingleOptionCompound,
    DialogInputsText,
    DialogInputsTextMultiline,
)
from dialog_ui.dialog_component.types import (
    DialogActionType,
    DialogActionTypeDynamic,
    DialogAfterActionOperation,
    DialogBodyType,
    DialogInputsType,
    DialogType,
    check_if_type_matched,
)


@dataclass
class DialogBase:
    """An base class of Minecraft dialog component.

    .. warning::
       Do not use `dataclass.asdict()` to convert this class to a dict, as it will not convert the correct data structure for the dialog component.
       Instead, use the `to_dict()` method provided in this class.

    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    @property
    @abstractmethod
    def type(self) -> DialogType:
        """One dialog types from the `minecraft:dialog_type` registry.
        """
        ...

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

    body: list[DialogBodyBase] | DialogBodyBase | None = None
    """Optional list of body elements or a single body element.
    `Ref: <https://minecraft.wiki/w/Dialog#Body_format>`__"""

    inputs: list[DialogInputsBase] | None = None
    """Optional list of input controls.
    `Ref: <https://minecraft.wiki/w/Dialog#Input_control_format>`__"""

    def to_dict(self) -> dict:
        """Convert the dataclass to a dict with correct data structure for the dialog component."""
        result: dict[str, Any] = {
            "type": self.type.value,
            "title": self.title.to_json_object(),
            "can_close_with_escape": self.can_close_with_escape,
            "pause": self.pause,
            "after_action": self.after_action.value,
        }
        if self.external_title is not None:
            result["external_title"] = self.external_title.to_json_object()
        if self.body is not None:
            if isinstance(self.body, list):
                result["body"] = [element.to_dict() for element in cast(list[DialogBodyBase], self.body)]
            else:
                result["body"] = self.body.to_dict()
        if self.inputs is not None:
            result["inputs"] = [input_control.to_dict() for input_control in self.inputs]
        return result

    @classmethod
    def _parse_base_kwargs(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Parse base class fields from dict, returning a dict of kwargs for __init__."""
        after_action_option = data.get("after_action", "close")
        after_action = DialogAfterActionOperation(after_action_option)
        title = RTextBase.from_json_object(data["title"])
        external_title = None
        if data.get("external_title", None):
            external_title = RTextBase.from_json_object(data["external_title"])
        body = None
        if data.get("body", None):
            body_data = data["body"]
            if isinstance(body_data, list):
                body = [DialogBodyBase.from_dict(item) for item in body_data]
            elif isinstance(body_data, dict):
                body = DialogBodyBase.from_dict(body_data)
            else:
                body = body_data
        inputs = None
        if data.get("inputs", None):
            inputs = [DialogInputsBase.from_dict(item) for item in data["inputs"]]
        return {
            "title": title,
            "can_close_with_escape": data.get("can_close_with_escape", True),
            "pause": data.get("pause", True),
            "after_action": after_action,
            "external_title": external_title,
            "body": body,
            "inputs": inputs,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DialogBase:
        _dialog_type_dispatch: dict[str, type[DialogBase]] = {
            DialogType.NOTICE.value: DialogNotice,
            DialogType.CONFIRMATION.value: DialogConfirmation,
            DialogType.MULTI_ACTION.value: DialogMultiAction,
            DialogType.SERVER_LINKS.value: DialogServerLinks,
            DialogType.DIALOG_LIST.value: DialogList,
        }
        dialog_type = data.get("type", "")
        dialog_cls = _dialog_type_dispatch.get(dialog_type)
        if dialog_cls is None:
            raise ValueError(f"Unknown dialog type: {dialog_type}")
        return dialog_cls.from_dict(data)


@dataclass
class DialogNoticeAction:
    label: RTextBase = field(default_factory=lambda: RText("gui.ok"))
    tooltip: RTextBase | None = None
    width: int | None = None
    action: DialogAction | None = None

    def to_dict(self) -> dict:
        result: dict[str, Any] = {
            "label": self.label.to_json_object(),
        }
        if self.tooltip:
            result.update({"tooltip": self.tooltip.to_json_object()})
        if self.width is not None:
            result.update({"width": self.width})
        if self.action:
            result.update({"action": self.action.to_dict()})
        return result
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            label=RTextBase.from_json_object(data["label"]),
            tooltip=RTextBase.from_json_object(data["tooltip"]) if "tooltip" in data else None,
            width=data.get("width", None),
            action=DialogAction.from_dict(data["action"]) if "action" in data else None,
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
        kwargs["action"] = DialogNoticeAction.from_dict(data["action"]) if "action" in data else None
        return cls(**kwargs)


@dataclass
class DialogConfirmation(DialogBase):
    _type: DialogType = field(init=False, default=DialogType.CONFIRMATION)

    @property
    def type(self) -> DialogType:
        return self._type

    yes: DialogNoticeAction = field(default_factory=lambda: DialogNoticeAction(label=RText("Yes")))
    no: DialogNoticeAction = field(default_factory=lambda: DialogNoticeAction(label=RText("No")))

    def to_dict(self) -> dict:
        result: dict[str, Any] = super().to_dict()
        result.update({
            "yes": self.yes.to_dict(),
            "no": self.no.to_dict(),
        })
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
        result.update({
            "actions": [action.to_dict() for action in self.actions],
        })
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
        kwargs["actions"] = [DialogNoticeAction.from_dict(action) for action in data["actions"]]
        kwargs["columns"] = data.get("columns", None)
        kwargs["exit_action"] = DialogNoticeAction.from_dict(data["exit_action"]) if "exit_action" in data else None
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
        kwargs["exit_action"] = DialogNoticeAction.from_dict(data["exit_action"]) if "exit_action" in data else None
        kwargs["columns"] = data.get("columns", None)
        kwargs["button_width"] = data.get("button_width", None)
        return cls(**kwargs)


@dataclass
class DialogList(DialogBase):
    _type: DialogType = field(init=False, default=DialogType.DIALOG_LIST)

    @property
    def type(self) -> DialogType:
        return self._type
    
    dialogs: str | list[DialogBase | str] | DialogBase
    exit_action: DialogNoticeAction | None = None
    columns: int | None = None
    button_width: int | None = None

    def to_dict(self) -> dict:
        result: dict[str, Any] = super().to_dict()
        if isinstance(self.dialogs, str):
            result.update({"dialogs": self.dialogs})
        elif isinstance(self.dialogs, list):
            result.update({"dialogs": [dialog.to_dict() if isinstance(dialog, DialogBase) else dialog for dialog in self.dialogs]})
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
        kwargs["exit_action"] = DialogNoticeAction.from_dict(data["exit_action"]) if "exit_action" in data else None
        kwargs["columns"] = data.get("columns", None)
        kwargs["button_width"] = data.get("button_width", None)
        return cls(**kwargs)


__all__ = [
    "DialogAction",
    # Action classes
    "DialogActionBase",
    "DialogActionChangePage",
    "DialogActionCopyToClipboard",
    "DialogActionCustom",
    "DialogActionCustomDynamic",
    "DialogActionOpenUrl",
    "DialogActionRunCommand",
    "DialogActionRunCommandDynamic",
    "DialogActionShowDialog",
    "DialogActionSuggestCommand",
    "DialogActionType",
    "DialogActionTypeDynamic",
    "DialogAfterActionOperation",
    "DialogBase",
    # Body classes
    "DialogBodyBase",
    "DialogBodyItem",
    "DialogBodyItemDescription",
    "DialogBodyItemObject",
    "DialogBodyPlainMessage",
    "DialogBodyType",
    # Dialog classes
    "DialogConfirmation",
    # Input classes
    "DialogInputsBase",
    "DialogInputsBoolean",
    "DialogInputsNumberRange",
    "DialogInputsSingleOption",
    "DialogInputsSingleOptionCompound",
    "DialogInputsText",
    "DialogInputsTextMultiline",
    "DialogInputsType",
    "DialogList",
    "DialogMultiAction",
    "DialogNotice",
    "DialogNoticeAction",
    "DialogServerLinks",
    # Types
    "DialogType",
    "check_if_type_matched",
]

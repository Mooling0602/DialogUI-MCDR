from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Self, cast

from mcdreforged.api.all import RText, RTextBase

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
class DialogActionBase:
    @property
    @abstractmethod
    def type(self) -> DialogActionType | DialogActionTypeDynamic: ...

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError("DialogActionBase does not support serialization, please use the specific dialog action class instead.")
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DialogActionBase:
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
            "dialog": self.dialog.to_dict() if isinstance(self.dialog, DialogBase) else self.dialog,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(_type, DialogActionType.SHOW_DIALOG.value):
            raise ValueError("Invalid type for DialogActionShowDialog")
        return cls(
            dialog=data["dialog"]
        )


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
        if not _type or not check_if_type_matched(_type, DialogActionType.OPEN_URL.value):
            raise ValueError("Invalid type for DialogActionOpenUrl")
        return cls(
            url=data["url"]
        )


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
        if not _type or not check_if_type_matched(_type, DialogActionType.RUN_COMMAND.value):
            raise ValueError("Invalid type for DialogActionRunCommand")
        return cls(
            command=data["command"]
        )


@dataclass
class DialogActionSuggestCommand(DialogActionBase):
    _type: DialogActionType = field(init=False, default=DialogActionType.SUGGEST_COMMAND)
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
        if not _type or not check_if_type_matched(_type, DialogActionType.SUGGEST_COMMAND.value):
            raise ValueError("Invalid type for DialogActionSuggestCommand")
        return cls(
            command=data["command"]
        )

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
        if not _type or not check_if_type_matched(_type, DialogActionType.CHANGE_PAGE.value):
            raise ValueError("Invalid type for DialogActionChangePage")
        return cls(
            page=data["page"]
        )


@dataclass
class DialogActionCopyToClipboard(DialogActionBase):
    _type: DialogActionType = field(init=False, default=DialogActionType.COPY_TO_CLIPBOARD)
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
        if not _type or not check_if_type_matched(_type, DialogActionType.COPY_TO_CLIPBOARD.value):
            raise ValueError("Invalid type for DialogActionCopyToClipboard")
        return cls(
            value=data["value"]
        )


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
    _type: DialogActionTypeDynamic = field(init=False, default=DialogActionTypeDynamic.RUN_COMMAND)
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
        if not _type or not check_if_type_matched(_type, DialogActionTypeDynamic.RUN_COMMAND.value):
            raise ValueError("Invalid type for DialogActionRunCommandDynamic")
        return cls(
            template=data["template"]
        )


@dataclass
class DialogActionCustomDynamic(DialogActionBase):
    _type: DialogActionTypeDynamic = field(init=False, default=DialogActionTypeDynamic.CUSTOM)
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
        if not _type or not check_if_type_matched(_type, DialogActionTypeDynamic.CUSTOM.value):
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


@dataclass
class DialogBodyBase:
    """An base class of Minecraft dialog body component."""

    @property
    @abstractmethod
    def type(self) -> DialogBodyType:
        """One dialog body types from the `minecraft:body_type` registry.
        """
        ...

    def to_dict(self) -> dict:
        raise NotImplementedError("DialogBodyBase does not support serialization, please use the specific dialog body class instead.")
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DialogBodyBase:
        _body_type_dispatch: dict[str, type[DialogBodyBase]] = {
            DialogBodyType.PLAIN_MESSAGE.value: DialogBodyPlainMessage,
            DialogBodyType.ITEM.value: DialogBodyItem,
        }
        body_type = data.get("type", "")
        body_cls = _body_type_dispatch.get(body_type)
        if body_cls is None:
            raise ValueError(f"Unknown body type: {body_type}")
        return body_cls.from_dict(data)


@dataclass
class DialogBodyPlainMessage(DialogBodyBase):
    _type: DialogBodyType = field(init=False, default=DialogBodyType.PLAIN_MESSAGE)

    @property
    def type(self) -> DialogBodyType:
        return self._type
    
    contents: RTextBase
    width: int | None = None

    def to_dict(self) -> dict:
        result: dict[str, Any] = {
            "type": self.type.value,
        }
        result.update({
            "contents": self.contents.to_json_object(),
        })
        if self.width is not None:
            result.update({"width": self.width})
        return result
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(_type, DialogBodyType.PLAIN_MESSAGE.value):
            raise ValueError("Invalid type for DialogBodyPlainMessage")
        return cls(
            contents=RTextBase.from_json_object(data["contents"]),
            width=data.get("width", None),
        )


@dataclass
class DialogBodyItemDescription:
    contents: str | list[str | RTextBase] | RTextBase | None = None
    width: int | None = None

    def to_dict(self) -> dict:
        result = {}
        if self.contents:
            if isinstance(self.contents, RTextBase):
                result.update({"contents": self.contents.to_json_object()})
            elif isinstance(self.contents, list):
                result.update({"contents": [
                    item.to_json_object() if isinstance(item, RTextBase) else item
                    for item in self.contents
                ]})
            else:
                result.update({"contents": self.contents})
        if self.width is not None:
            result.update({"width": self.width})
        return result
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        contents = data.get("contents", None)
        if isinstance(contents, dict):
            contents = RTextBase.from_json_object(contents)
        elif isinstance(contents, list):
            contents = [
                RTextBase.from_json_object(item) if isinstance(item, dict) else item
                for item in contents
            ]
        return cls(
            contents=contents,
            width=data.get("width", None),
        )


@dataclass
class DialogBodyItemObject:
    id: str
    count: int | None = None
    components: dict[str, Any] | None = None

    def to_dict(self) -> dict:
        result = {}
        result.update({"id": self.id})
        if self.count is not None:
            result.update({"count": self.count})
        if self.components:
            result.update({"components": self.components})
        return result
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data["id"],
            count=data.get("count", None),
            components=data.get("components", None),
        )


@dataclass
class DialogBodyItem(DialogBodyBase):
    _type: DialogBodyType = field(init=False, default=DialogBodyType.ITEM)

    @property
    def type(self) -> DialogBodyType:
        return self._type
    
    item: DialogBodyItemObject
    description: str | list[str | RTextBase] | RTextBase | DialogBodyItemDescription | None = None
    show_decoration: bool = True
    show_tooltip: bool = True
    width: int | None = None
    height: int | None = None

    def to_dict(self) -> dict:
        result: dict[str, Any] = {
            "type": self.type.value,
        }
        
        # 处理 description 的序列化
        if self.description is None:
            description_serialized = None
        elif isinstance(self.description, DialogBodyItemDescription):
            description_serialized = self.description.to_dict()
        elif isinstance(self.description, RTextBase):
            description_serialized = self.description.to_json_object()
        elif isinstance(self.description, list):
            description_serialized = [
                item.to_json_object() if isinstance(item, RTextBase) else item
                for item in self.description
            ]
        else:
            description_serialized = self.description
        
        result.update({
            "item": self.item.to_dict(),
            "show_decoration": self.show_decoration,
            "show_tooltip": self.show_tooltip,
        })
        if self.description is not None:
            result["description"] = description_serialized
        if self.width is not None:
            result.update({"width": self.width})
        if self.height is not None:
            result.update({"height": self.height})
        return result
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(_type, DialogBodyType.ITEM.value):
            raise ValueError("Invalid type for DialogBodyItem")
        
        description: str | list[str | RTextBase] | RTextBase | DialogBodyItemDescription | None = None
        if "description" in data and data["description"] is not None:
            raw_desc = data["description"]
            if isinstance(raw_desc, dict) and "contents" in raw_desc:
                description = DialogBodyItemDescription.from_dict(raw_desc)
            elif isinstance(raw_desc, dict):
                description = RTextBase.from_json_object(raw_desc)
            elif isinstance(raw_desc, list):
                description = [
                    RTextBase.from_json_object(item) if isinstance(item, dict) else item
                    for item in raw_desc
                ]
            else:
                description = raw_desc
        
        return cls(
            item=DialogBodyItemObject.from_dict(data["item"]),
            description=description,
            show_decoration=data.get("show_decoration", True),
            show_tooltip=data.get("show_tooltip", True),
            width=data.get("width", None),
            height=data.get("height", None),
        )


@dataclass
class DialogInputsBase:
    @property
    @abstractmethod
    def type(self) -> DialogInputsType: ...

    key: str
    label: RTextBase

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "key": self.key,
            "label": self.label.to_json_object(),
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DialogInputsBase:
        _inputs_type_dispatch: dict[str, type[DialogInputsBase]] = {
            DialogInputsType.TEXT.value: DialogInputsText,
            DialogInputsType.BOOLEAN.value: DialogInputsBoolean,
            DialogInputsType.SINGLE_OPTION.value: DialogInputsSingleOption,
            DialogInputsType.NUMBER_RANGE.value: DialogInputsNumberRange,
        }
        inputs_type = data.get("type", "")
        inputs_cls = _inputs_type_dispatch.get(inputs_type)
        if inputs_cls is None:
            raise ValueError(f"Unknown inputs type: {inputs_type}")
        return inputs_cls.from_dict(data)


@dataclass
class DialogInputsTextMultiline:
    max_lines: int | None = None
    height: int | None = None

    def to_dict(self) -> dict:
        result = {}
        if self.max_lines is not None:
            result.update({"max_lines": self.max_lines})
        if self.height is not None:
            result.update({"height": self.height})
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            max_lines=data.get("max_lines", None),
            height=data.get("height", None),
        )


@dataclass
class DialogInputsText(DialogInputsBase):
    _type: DialogInputsType = field(init=False, default=DialogInputsType.TEXT)

    @property
    def type(self) -> DialogInputsType:
        return self._type

    width: int | None = None
    label_visible: bool = True
    initial: str | None = None
    max_length: int | None = None
    multiline: DialogInputsTextMultiline | None = None

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "label_visible": self.label_visible,
        })
        if self.width is not None:
            result["width"] = self.width
        if self.initial is not None:
            result["initial"] = self.initial
        if self.max_length is not None:
            result["max_length"] = self.max_length
        if self.multiline is not None:
            result["multiline"] = self.multiline.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            key=data["key"],
            label=RTextBase.from_json_object(data["label"]),
            width=data.get("width", None),
            label_visible=data.get("label_visible", True),
            initial=data.get("initial", None),
            max_length=data.get("max_length", None),
            multiline=DialogInputsTextMultiline.from_dict(data["multiline"]) if "multiline" in data else None,
        )


@dataclass
class DialogInputsBoolean(DialogInputsBase):
    _type: DialogInputsType = field(init=False, default=DialogInputsType.BOOLEAN)

    @property
    def type(self) -> DialogInputsType:
        return self._type

    initial: bool = False
    on_true: str | None = None
    on_false: str | None = None

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "initial": self.initial,
        })
        if self.on_true is not None:
            result["on_true"] = self.on_true
        if self.on_false is not None:
            result["on_false"] = self.on_false
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            key=data["key"],
            label=RTextBase.from_json_object(data["label"]),
            initial=data.get("initial", False),
            on_true=data.get("on_true", None),
            on_false=data.get("on_false", None),
        )


@dataclass
class DialogInputsSingleOptionCompound:
    id: str
    display: str | list[str | RTextBase] | RTextBase | None = None
    initial: bool | None = None

    def to_dict(self) -> dict:
        result = {}
        result.update({"id": self.id})
        if self.display:
            if isinstance(self.display, RTextBase):
                result.update({"display": self.display.to_json_object()})
            elif isinstance(self.display, list):
                result.update({"display": [item.to_json_object() if isinstance(item, RTextBase) else item for item in self.display]})
            else:
                result.update({"display": self.display})
        if self.initial is not None:
            result.update({"initial": self.initial})
        return result
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        display: str | list[str | RTextBase] | RTextBase | None = None
        if "display" in data:
            raw_display = data["display"]
            if isinstance(raw_display, list):
                display = [
                    RTextBase.from_json_object(item) if isinstance(item, dict) else item
                    for item in raw_display
                ]
            elif isinstance(raw_display, dict):
                display = RTextBase.from_json_object(raw_display)
            else:
                display = raw_display
        return cls(
            id=data["id"],
            display=display,
            initial=data.get("initial", None),
        )


@dataclass
class DialogInputsSingleOption(DialogInputsBase):
    _type: DialogInputsType = field(init=False, default=DialogInputsType.SINGLE_OPTION)

    @property
    def type(self) -> DialogInputsType:
        return self._type

    options: list[DialogInputsSingleOptionCompound]
    label_visible: bool = True
    width: int | None = None

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "options": [option.to_dict() for option in self.options],
            "label_visible": self.label_visible,
        })
        if self.width is not None:
            result["width"] = self.width
        return result
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            key=data["key"],
            label=RTextBase.from_json_object(data["label"]),
            options=[DialogInputsSingleOptionCompound.from_dict(option) for option in data["options"]],
            label_visible=data.get("label_visible", True),
            width=data.get("width", None),
        )


@dataclass
class DialogInputsNumberRange(DialogInputsBase):
    _type: DialogInputsType = field(init=False, default=DialogInputsType.NUMBER_RANGE)

    @property
    def type(self) -> DialogInputsType:
        return self._type
    
    start: float
    end: float
    label_format: str | None = None
    width: int | None = None
    step: float | None = None
    initial: float | None = None

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "start": self.start,
            "end": self.end,
        })
        if self.label_format is not None:
            result["label_format"] = self.label_format
        if self.width is not None:
            result["width"] = self.width
        if self.step is not None:
            result["step"] = self.step
        if self.initial is not None:
            result["initial"] = self.initial
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            key=data["key"],
            label=RTextBase.from_json_object(data["label"]),
            start=data["start"],
            end=data["end"],
            label_format=data.get("label_format", None),
            width=data.get("width", None),
            step=data.get("step", None),
            initial=data.get("initial", None),
        )


if __name__ == "__main__":
    pass  # impl simple test logic here.

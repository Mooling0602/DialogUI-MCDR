"""Base dialog classes - DialogBase and DialogNoticeAction.

Separated from __init__.py to break the circular import with action.py:
  base.py <-- action.py, dialogs.py (no cycle)
"""
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Self, cast

from mcdreforged.api.all import RText, RTextBase, RTextJsonFormat

from dialog_ui.dialog_component.body import DialogBodyBase
from dialog_ui.dialog_component.inputs import DialogInputsBase
from dialog_ui.dialog_component.types import (
    DialogAfterActionOperation,
    DialogType,
)

if TYPE_CHECKING:
    from dialog_ui.dialog_component.action import DialogAction


@dataclass
class DialogBase:
    """An base class of Minecraft dialog component.

    .. warning::
       Do not use ``dataclass.asdict()`` to convert this class to a dict, as it will not convert the correct data structure for the dialog component.
       Instead, use the ``to_dict()`` method provided in this class.

    `Ref: <https://minecraft.wiki/w/Dialog#Dialog_format>`__"""

    @property
    @abstractmethod
    def type(self) -> DialogType:
        """One dialog types from the ``minecraft:dialog_type`` registry."""
        ...

    title: RTextBase
    """The title text component of the dialog."""

    can_close_with_escape: bool = True
    """Can dialog be dismissed with Escape key. Defaults to ``true``."""

    pause: bool = True
    """If the dialog screen should pause the game in single-player mode. Defaults to ``true``."""

    after_action: DialogAfterActionOperation = DialogAfterActionOperation.CLOSE
    """An additional operation performed on the dialog after click or submit actions. Defaults to ``close``."""

    external_title: RTextBase | None = None
    """Name to be used for a button leading to this dialog (e.g. on the pause menu or in a parent ``dialog_list``), optional text component.
    If not present, ``title`` is used instead."""

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
            "title": self.title.to_json_object(json_format=RTextJsonFormat.V_1_21_5),
            "can_close_with_escape": self.can_close_with_escape,
            "pause": self.pause,
            "after_action": self.after_action.value,
        }
        if self.external_title is not None:
            result["external_title"] = self.external_title.to_json_object(json_format=RTextJsonFormat.V_1_21_5)
        if self.body is not None:
            if isinstance(self.body, list):
                result["body"] = [
                    element.to_dict()
                    for element in cast(list[DialogBodyBase], self.body)
                ]
            else:
                result["body"] = self.body.to_dict()
        if self.inputs is not None:
            result["inputs"] = [
                input_control.to_dict() for input_control in self.inputs
            ]
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
    def from_dict(cls, data: dict[str, Any]) -> "DialogBase":
        # Lazy import to avoid circular dependency with concrete dialog classes
        from dialog_ui.dialog_component.dialogs import (
            DialogConfirmation,
            DialogList,
            DialogMultiAction,
            DialogNotice,
            DialogServerLinks,
        )

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
    """Button entry used by notice, confirmation, multi-action, and exit actions.

    `Ref: <https://minecraft.wiki/w/Dialog#notice>`__
    """

    label: RTextBase = field(default_factory=lambda: RText("gui.ok"))
    """Button label text component."""

    tooltip: RTextBase | None = None
    """Optional tooltip shown when the button is highlighted or hovered."""

    width: int | None = None
    """Button width. Defaults to Minecraft's own value."""

    action: "DialogAction | None" = None
    """Optional action payload performed when the button is clicked."""

    def to_dict(self) -> dict:
        result: dict[str, Any] = {
            "label": self.label.to_json_object(json_format=RTextJsonFormat.V_1_21_5),
        }
        if self.tooltip:
            result.update({"tooltip": self.tooltip.to_json_object(json_format=RTextJsonFormat.V_1_21_5)})
        if self.width is not None:
            result.update({"width": self.width})
        if self.action:
            result.update({"action": self.action.to_dict()})
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        # Lazy import to avoid circular dependency with action.py
        from dialog_ui.dialog_component.action import DialogAction

        return cls(
            label=RTextBase.from_json_object(data["label"]),
            tooltip=RTextBase.from_json_object(data["tooltip"])
            if "tooltip" in data
            else None,
            width=data.get("width", None),
            action=DialogAction.from_dict(data["action"]) if "action" in data else None,
        )

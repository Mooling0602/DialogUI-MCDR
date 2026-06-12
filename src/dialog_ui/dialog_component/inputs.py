"""Dialog input control classes matching Minecraft dialog input format.

`Ref: <https://minecraft.wiki/w/Dialog#Input_control_format>`__
"""

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Self

from mcdreforged.api.all import RTextBase, RTextJsonFormat

from dialog_ui.dialog_component.types import DialogInputsType


@dataclass
class DialogInputsBase:
    """Base class for input controls that submit values by key."""

    @property
    @abstractmethod
    def type(self) -> DialogInputsType:
        """One input control type from the ``minecraft:input_control_type`` registry."""
        ...

    key: str
    """Identifier used to reference the submitted value."""

    label: RTextBase
    """Text component displayed next to the input control."""

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "key": self.key,
            "label": self.label.to_json_object(json_format=RTextJsonFormat.V_1_21_5),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DialogInputsBase":
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
    """Configuration that turns a text input into a multiline input.

    `Ref: <https://minecraft.wiki/w/Dialog#text>`__
    """

    max_lines: int | None = None
    """Maximum number of input lines."""

    height: int | None = None
    """Height of the multiline input."""

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
    """A single-line or multiline text input control.

    `Ref: <https://minecraft.wiki/w/Dialog#text>`__
    """

    _type: DialogInputsType = field(init=False, default=DialogInputsType.TEXT)

    @property
    def type(self) -> DialogInputsType:
        return self._type

    width: int | None = None
    """Width of the input. Defaults to Minecraft's own value."""

    label_visible: bool = True
    """Whether the label is visible. Defaults to ``true``."""

    initial: str | None = None
    """Initial text value."""

    max_length: int | None = None
    """Maximum input length."""

    multiline: DialogInputsTextMultiline | None = None
    """Optional multiline input configuration."""

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update(
            {
                "label_visible": self.label_visible,
            }
        )
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
            multiline=DialogInputsTextMultiline.from_dict(data["multiline"])
            if "multiline" in data
            else None,
        )


@dataclass
class DialogInputsBoolean(DialogInputsBase):
    """A checkbox input control.

    `Ref: <https://minecraft.wiki/w/Dialog#boolean>`__
    """

    _type: DialogInputsType = field(init=False, default=DialogInputsType.BOOLEAN)

    @property
    def type(self) -> DialogInputsType:
        return self._type

    initial: bool = False
    """Initial checked state. Defaults to ``false``."""

    on_true: str | None = None
    """Template substitution value sent when checked."""

    on_false: str | None = None
    """Template substitution value sent when unchecked."""

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update(
            {
                "initial": self.initial,
            }
        )
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
    """One selectable option in a single-option input control.

    `Ref: <https://minecraft.wiki/w/Dialog#single_option>`__
    """

    id: str
    """Value sent when this option is selected."""

    display: str | list[str | RTextBase] | RTextBase | None = None
    """Text component displayed for this option."""

    initial: bool | None = None
    """Whether this option is selected initially."""

    def to_dict(self) -> dict:
        result = {}
        result.update({"id": self.id})
        if self.display:
            if isinstance(self.display, RTextBase):
                result.update({"display": self.display.to_json_object(json_format=RTextJsonFormat.V_1_21_5)})
            elif isinstance(self.display, list):
                result.update(
                    {
                        "display": [
                            item.to_json_object(json_format=RTextJsonFormat.V_1_21_5)
                            if isinstance(item, RTextBase)
                            else item
                            for item in self.display
                        ]
                    }
                )
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
    """A preset option selection input control.

    `Ref: <https://minecraft.wiki/w/Dialog#single_option>`__
    """

    _type: DialogInputsType = field(init=False, default=DialogInputsType.SINGLE_OPTION)

    @property
    def type(self) -> DialogInputsType:
        return self._type

    options: list[DialogInputsSingleOptionCompound]
    """Non-empty list of selectable options."""

    label_visible: bool = True
    """Whether the label is visible. Defaults to ``true``."""

    width: int | None = None
    """Width of the input. Defaults to Minecraft's own value."""

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update(
            {
                "options": [option.to_dict() for option in self.options],
                "label_visible": self.label_visible,
            }
        )
        if self.width is not None:
            result["width"] = self.width
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            key=data["key"],
            label=RTextBase.from_json_object(data["label"]),
            options=[
                DialogInputsSingleOptionCompound.from_dict(option)
                for option in data["options"]
            ],
            label_visible=data.get("label_visible", True),
            width=data.get("width", None),
        )


@dataclass
class DialogInputsNumberRange(DialogInputsBase):
    """A number slider input control.

    `Ref: <https://minecraft.wiki/w/Dialog#number_range>`__
    """

    _type: DialogInputsType = field(init=False, default=DialogInputsType.NUMBER_RANGE)

    @property
    def type(self) -> DialogInputsType:
        return self._type

    start: float
    """Minimum slider value."""

    end: float
    """Maximum slider value."""

    label_format: str | None = None
    """Translation key used to build the displayed label."""

    width: int | None = None
    """Width of the input. Defaults to Minecraft's own value."""

    step: float | None = None
    """Step size for allowed slider values."""

    initial: float | None = None
    """Initial slider value. Defaults to the middle of the range."""

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update(
            {
                "start": self.start,
                "end": self.end,
            }
        )
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

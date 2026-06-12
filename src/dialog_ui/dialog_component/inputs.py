from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Self

from mcdreforged.api.all import RTextBase

from dialog_ui.dialog_component.types import DialogInputsType


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
    _type: DialogInputsType = field(init=False, default=DialogInputsType.BOOLEAN)

    @property
    def type(self) -> DialogInputsType:
        return self._type

    initial: bool = False
    on_true: str | None = None
    on_false: str | None = None

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
                result.update(
                    {
                        "display": [
                            item.to_json_object()
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
    _type: DialogInputsType = field(init=False, default=DialogInputsType.SINGLE_OPTION)

    @property
    def type(self) -> DialogInputsType:
        return self._type

    options: list[DialogInputsSingleOptionCompound]
    label_visible: bool = True
    width: int | None = None

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

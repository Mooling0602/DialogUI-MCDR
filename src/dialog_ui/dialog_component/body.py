from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Self

from mcdreforged.api.all import RTextBase

from dialog_ui.dialog_component.types import DialogBodyType, check_if_type_matched


@dataclass
class DialogBodyBase:
    """An base class of Minecraft dialog body component."""

    @property
    @abstractmethod
    def type(self) -> DialogBodyType:
        """One dialog body types from the `minecraft:body_type` registry."""
        ...

    def to_dict(self) -> dict:
        raise NotImplementedError(
            "DialogBodyBase does not support serialization, please use the specific dialog body class instead."
        )

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
        result.update(
            {
                "contents": self.contents.to_json_object(),
            }
        )
        if self.width is not None:
            result.update({"width": self.width})
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        _type = data.get("type")
        if not _type or not check_if_type_matched(
            _type, DialogBodyType.PLAIN_MESSAGE.value
        ):
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
                result.update(
                    {
                        "contents": [
                            item.to_json_object()
                            if isinstance(item, RTextBase)
                            else item
                            for item in self.contents
                        ]
                    }
                )
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
    description: (
        str | list[str | RTextBase] | RTextBase | DialogBodyItemDescription | None
    ) = None
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

        result.update(
            {
                "item": self.item.to_dict(),
                "show_decoration": self.show_decoration,
                "show_tooltip": self.show_tooltip,
            }
        )
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

        description: (
            str | list[str | RTextBase] | RTextBase | DialogBodyItemDescription | None
        ) = None
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

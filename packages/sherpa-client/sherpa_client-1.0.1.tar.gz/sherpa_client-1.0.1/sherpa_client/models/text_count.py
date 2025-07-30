from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="TextCount")


@_attrs_define
class TextCount:
    """
    Attributes:
        field_id (str):
        count (int):
    """

    field_id: str
    count: int

    def to_dict(self) -> dict[str, Any]:
        field_id = self.field_id

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "_id": field_id,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field_id = d.pop("_id")

        count = d.pop("count")

        text_count = cls(
            field_id=field_id,
            count=count,
        )

        return text_count

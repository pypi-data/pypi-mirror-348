from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ItemCount")


@_attrs_define
class ItemCount:
    """
    Attributes:
        count (int):
        name (str):
    """

    count: int
    name: str

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "count": count,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        name = d.pop("name")

        item_count = cls(
            count=count,
            name=name,
        )

        return item_count

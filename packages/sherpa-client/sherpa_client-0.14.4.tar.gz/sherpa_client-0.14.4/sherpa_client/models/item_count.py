from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ItemCount")


@attr.s(auto_attribs=True)
class ItemCount:
    """
    Attributes:
        count (int):
        name (str):
    """

    count: int
    name: str

    def to_dict(self) -> Dict[str, Any]:
        count = self.count
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "count": count,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        count = d.pop("count")

        name = d.pop("name")

        item_count = cls(
            count=count,
            name=name,
        )

        return item_count

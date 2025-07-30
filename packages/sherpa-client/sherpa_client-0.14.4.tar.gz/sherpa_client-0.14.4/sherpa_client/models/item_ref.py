from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ItemRef")


@attr.s(auto_attribs=True)
class ItemRef:
    """
    Attributes:
        name (str):
    """

    name: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        item_ref = cls(
            name=name,
        )

        return item_ref

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CategoryAction")


@_attrs_define
class CategoryAction:
    """
    Attributes:
        add (bool): add or remove
        label_name (str): category label name
    """

    add: bool
    label_name: str

    def to_dict(self) -> dict[str, Any]:
        add = self.add

        label_name = self.label_name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "add": add,
                "labelName": label_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        add = d.pop("add")

        label_name = d.pop("labelName")

        category_action = cls(
            add=add,
            label_name=label_name,
        )

        return category_action

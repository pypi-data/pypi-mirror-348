from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SimpleGroupMembershipDesc")


@_attrs_define
class SimpleGroupMembershipDesc:
    """
    Attributes:
        label (str):
        name (str):
    """

    label: str
    name: str

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        name = d.pop("name")

        simple_group_membership_desc = cls(
            label=label,
            name=name,
        )

        return simple_group_membership_desc

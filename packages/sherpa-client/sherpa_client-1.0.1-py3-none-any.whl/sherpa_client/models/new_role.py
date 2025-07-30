from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="NewRole")


@_attrs_define
class NewRole:
    """
    Attributes:
        label (str):
        permissions (list[str]):
    """

    label: str
    permissions: list[str]

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        permissions = self.permissions

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        permissions = cast(list[str], d.pop("permissions"))

        new_role = cls(
            label=label,
            permissions=permissions,
        )

        return new_role

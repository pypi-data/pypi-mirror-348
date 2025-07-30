from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RoleUpdate")


@_attrs_define
class RoleUpdate:
    """
    Attributes:
        label (Union[Unset, str]):
        permissions (Union[Unset, list[str]]):
    """

    label: Union[Unset, str] = UNSET
    permissions: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        permissions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label", UNSET)

        permissions = cast(list[str], d.pop("permissions", UNSET))

        role_update = cls(
            label=label,
            permissions=permissions,
        )

        return role_update

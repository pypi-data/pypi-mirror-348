from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserPermissionsUpdate")


@_attrs_define
class UserPermissionsUpdate:
    """
    Attributes:
        disabled (Union[Unset, bool]):
        permissions (Union[Unset, list[str]]):
        roles (Union[Unset, list[str]]):
    """

    disabled: Union[Unset, bool] = UNSET
    permissions: Union[Unset, list[str]] = UNSET
    roles: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        disabled = self.disabled

        permissions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions

        roles: Union[Unset, list[str]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if roles is not UNSET:
            field_dict["roles"] = roles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        disabled = d.pop("disabled", UNSET)

        permissions = cast(list[str], d.pop("permissions", UNSET))

        roles = cast(list[str], d.pop("roles", UNSET))

        user_permissions_update = cls(
            disabled=disabled,
            permissions=permissions,
            roles=roles,
        )

        return user_permissions_update

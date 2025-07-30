from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewUser")


@_attrs_define
class NewUser:
    """
    Attributes:
        password (str):
        username (str):
        email (Union[Unset, str]):
        permissions (Union[Unset, list[str]]):
        roles (Union[Unset, list[str]]):
    """

    password: str
    username: str
    email: Union[Unset, str] = UNSET
    permissions: Union[Unset, list[str]] = UNSET
    roles: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        password = self.password

        username = self.username

        email = self.email

        permissions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions

        roles: Union[Unset, list[str]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "password": password,
                "username": username,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if roles is not UNSET:
            field_dict["roles"] = roles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        password = d.pop("password")

        username = d.pop("username")

        email = d.pop("email", UNSET)

        permissions = cast(list[str], d.pop("permissions", UNSET))

        roles = cast(list[str], d.pop("roles", UNSET))

        new_user = cls(
            password=password,
            username=username,
            email=email,
            permissions=permissions,
            roles=roles,
        )

        return new_user

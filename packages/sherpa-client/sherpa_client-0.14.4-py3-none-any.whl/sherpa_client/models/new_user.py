from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewUser")


@attr.s(auto_attribs=True)
class NewUser:
    """
    Attributes:
        password (str):
        username (str):
        email (Union[Unset, str]):
        permissions (Union[Unset, List[str]]):
        roles (Union[Unset, List[str]]):
    """

    password: str
    username: str
    email: Union[Unset, str] = UNSET
    permissions: Union[Unset, List[str]] = UNSET
    roles: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        password = self.password
        username = self.username
        email = self.email
        permissions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions

        roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles

        field_dict: Dict[str, Any] = {}
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        password = d.pop("password")

        username = d.pop("username")

        email = d.pop("email", UNSET)

        permissions = cast(List[str], d.pop("permissions", UNSET))

        roles = cast(List[str], d.pop("roles", UNSET))

        new_user = cls(
            password=password,
            username=username,
            email=email,
            permissions=permissions,
            roles=roles,
        )

        return new_user

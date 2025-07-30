from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserProfileUpdate")


@_attrs_define
class UserProfileUpdate:
    """
    Attributes:
        email (Union[Unset, str]):
        password (Union[Unset, str]):
        profilename (Union[Unset, str]):
    """

    email: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    profilename: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        password = self.password

        profilename = self.profilename

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if password is not UNSET:
            field_dict["password"] = password
        if profilename is not UNSET:
            field_dict["profilename"] = profilename

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email", UNSET)

        password = d.pop("password", UNSET)

        profilename = d.pop("profilename", UNSET)

        user_profile_update = cls(
            email=email,
            password=password,
            profilename=profilename,
        )

        return user_profile_update

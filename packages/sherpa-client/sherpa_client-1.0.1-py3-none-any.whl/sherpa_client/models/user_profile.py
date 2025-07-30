from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserProfile")


@_attrs_define
class UserProfile:
    """
    Attributes:
        profilename (str):
        username (str):
        email (Union[Unset, str]):
    """

    profilename: str
    username: str
    email: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        profilename = self.profilename

        username = self.username

        email = self.email

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "profilename": profilename,
                "username": username,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        profilename = d.pop("profilename")

        username = d.pop("username")

        email = d.pop("email", UNSET)

        user_profile = cls(
            profilename=profilename,
            username=username,
            email=email,
        )

        return user_profile

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SimpleUser")


@_attrs_define
class SimpleUser:
    """
    Attributes:
        profilename (str):
        username (str):
    """

    profilename: str
    username: str

    def to_dict(self) -> dict[str, Any]:
        profilename = self.profilename

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "profilename": profilename,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        profilename = d.pop("profilename")

        username = d.pop("username")

        simple_user = cls(
            profilename=profilename,
            username=username,
        )

        return simple_user

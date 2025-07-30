from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UserGroupRef")


@_attrs_define
class UserGroupRef:
    """
    Attributes:
        group_name (str):
        username (str):
    """

    group_name: str
    username: str

    def to_dict(self) -> dict[str, Any]:
        group_name = self.group_name

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "groupName": group_name,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        group_name = d.pop("groupName")

        username = d.pop("username")

        user_group_ref = cls(
            group_name=group_name,
            username=username,
        )

        return user_group_ref

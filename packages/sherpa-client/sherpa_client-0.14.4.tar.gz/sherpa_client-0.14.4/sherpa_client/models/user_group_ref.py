from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="UserGroupRef")


@attr.s(auto_attribs=True)
class UserGroupRef:
    """
    Attributes:
        group_name (str):
        username (str):
    """

    group_name: str
    username: str

    def to_dict(self) -> Dict[str, Any]:
        group_name = self.group_name
        username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "groupName": group_name,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        group_name = d.pop("groupName")

        username = d.pop("username")

        user_group_ref = cls(
            group_name=group_name,
            username=username,
        )

        return user_group_ref

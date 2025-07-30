from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="SimpleUser")


@attr.s(auto_attribs=True)
class SimpleUser:
    """
    Attributes:
        profilename (str):
        username (str):
    """

    profilename: str
    username: str

    def to_dict(self) -> Dict[str, Any]:
        profilename = self.profilename
        username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "profilename": profilename,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        profilename = d.pop("profilename")

        username = d.pop("username")

        simple_user = cls(
            profilename=profilename,
            username=username,
        )

        return simple_user

from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BearerToken")


@attr.s(auto_attribs=True)
class BearerToken:
    """
    Attributes:
        access_token (str):
        username (Union[Unset, str]):
    """

    access_token: str
    username: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        access_token = self.access_token
        username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "access_token": access_token,
            }
        )
        if username is not UNSET:
            field_dict["email"] = username

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        access_token = d.pop("access_token")

        username = d.pop("username", UNSET)

        bearer_token = cls(
            access_token=access_token,
            username=username,
        )

        return bearer_token

from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="BearerToken")


@_attrs_define
class BearerToken:
    """
    Attributes:
        access_token (str):
        email (Union[Unset, str]):
    """

    access_token: str
    email: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        access_token = self.access_token

        email = self.email

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "access_token": access_token,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        access_token = d.pop("access_token")

        email = d.pop("email", UNSET)

        bearer_token = cls(
            access_token=access_token,
            email=email,
        )

        return bearer_token

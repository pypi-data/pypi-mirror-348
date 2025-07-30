from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="BearerToken")


@_attrs_define
class BearerToken:
    """
    Attributes:
        access_token (str):
        email (str):
    """

    access_token: str
    email: str

    def to_dict(self) -> dict[str, Any]:
        access_token = self.access_token

        email = self.email

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "access_token": access_token,
                "email": email,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        access_token = d.pop("access_token")

        email = d.pop("email")

        bearer_token = cls(
            access_token=access_token,
            email=email,
        )

        return bearer_token

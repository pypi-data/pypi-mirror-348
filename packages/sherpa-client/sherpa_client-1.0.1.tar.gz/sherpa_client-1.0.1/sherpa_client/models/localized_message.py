from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="LocalizedMessage")


@_attrs_define
class LocalizedMessage:
    """
    Attributes:
        body (str):
        title (str):
    """

    body: str
    title: str

    def to_dict(self) -> dict[str, Any]:
        body = self.body

        title = self.title

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "body": body,
                "title": title,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        body = d.pop("body")

        title = d.pop("title")

        localized_message = cls(
            body=body,
            title=title,
        )

        return localized_message

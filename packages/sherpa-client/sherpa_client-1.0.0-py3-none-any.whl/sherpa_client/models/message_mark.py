from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="MessageMark")


@_attrs_define
class MessageMark:
    """
    Attributes:
        read (bool):
    """

    read: bool

    def to_dict(self) -> dict[str, Any]:
        read = self.read

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "read": read,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        read = d.pop("read")

        message_mark = cls(
            read=read,
        )

        return message_mark

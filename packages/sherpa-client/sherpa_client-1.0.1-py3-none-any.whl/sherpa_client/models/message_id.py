from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="MessageId")


@_attrs_define
class MessageId:
    """
    Attributes:
        id (str):
    """

    id: str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        message_id = cls(
            id=id,
        )

        return message_id

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CreatedByCount")


@_attrs_define
class CreatedByCount:
    """
    Attributes:
        count (int):
        created_by (str):
    """

    count: int
    created_by: str

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        created_by = self.created_by

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "count": count,
                "createdBy": created_by,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        created_by = d.pop("createdBy")

        created_by_count = cls(
            count=count,
            created_by=created_by,
        )

        return created_by_count

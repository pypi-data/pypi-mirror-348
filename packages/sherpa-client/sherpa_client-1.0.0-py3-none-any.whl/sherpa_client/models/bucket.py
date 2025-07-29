from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="Bucket")


@_attrs_define
class Bucket:
    """
    Attributes:
        doc_count (int):
        key (str):
    """

    doc_count: int
    key: str

    def to_dict(self) -> dict[str, Any]:
        doc_count = self.doc_count

        key = self.key

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "doc_count": doc_count,
                "key": key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        doc_count = d.pop("doc_count")

        key = d.pop("key")

        bucket = cls(
            doc_count=doc_count,
            key=key,
        )

        return bucket

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="MetadataCount")


@_attrs_define
class MetadataCount:
    """
    Attributes:
        field_id (str):
        document_count (int):
        segment_count (int):
    """

    field_id: str
    document_count: int
    segment_count: int

    def to_dict(self) -> dict[str, Any]:
        field_id = self.field_id

        document_count = self.document_count

        segment_count = self.segment_count

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "_id": field_id,
                "documentCount": document_count,
                "segmentCount": segment_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field_id = d.pop("_id")

        document_count = d.pop("documentCount")

        segment_count = d.pop("segmentCount")

        metadata_count = cls(
            field_id=field_id,
            document_count=document_count,
            segment_count=segment_count,
        )

        return metadata_count

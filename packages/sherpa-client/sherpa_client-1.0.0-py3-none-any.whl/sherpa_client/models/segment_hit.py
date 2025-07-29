from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.segment import Segment


T = TypeVar("T", bound="SegmentHit")


@_attrs_define
class SegmentHit:
    """
    Attributes:
        field_id (str):
        score (float):
        segment (Segment):
    """

    field_id: str
    score: float
    segment: "Segment"

    def to_dict(self) -> dict[str, Any]:
        field_id = self.field_id

        score = self.score

        segment = self.segment.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "_id": field_id,
                "score": score,
                "segment": segment,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.segment import Segment

        d = dict(src_dict)
        field_id = d.pop("_id")

        score = d.pop("score")

        segment = Segment.from_dict(d.pop("segment"))

        segment_hit = cls(
            field_id=field_id,
            score=score,
            segment=segment,
        )

        return segment_hit

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.document import Document


T = TypeVar("T", bound="DocumentHit")


@_attrs_define
class DocumentHit:
    """
    Attributes:
        field_id (str):
        document (Document):
        score (float):
    """

    field_id: str
    document: "Document"
    score: float

    def to_dict(self) -> dict[str, Any]:
        field_id = self.field_id

        document = self.document.to_dict()

        score = self.score

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "_id": field_id,
                "document": document,
                "score": score,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.document import Document

        d = dict(src_dict)
        field_id = d.pop("_id")

        document = Document.from_dict(d.pop("document"))

        score = d.pop("score")

        document_hit = cls(
            field_id=field_id,
            document=document,
            score=score,
        )

        return document_hit

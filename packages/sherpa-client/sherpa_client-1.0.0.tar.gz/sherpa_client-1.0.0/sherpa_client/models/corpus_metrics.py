from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.document_facets import DocumentFacets


T = TypeVar("T", bound="CorpusMetrics")


@_attrs_define
class CorpusMetrics:
    """
    Attributes:
        corpus_size (int):
        document_count (int):
        document_facets (DocumentFacets):
        segment_count (int):
    """

    corpus_size: int
    document_count: int
    document_facets: "DocumentFacets"
    segment_count: int

    def to_dict(self) -> dict[str, Any]:
        corpus_size = self.corpus_size

        document_count = self.document_count

        document_facets = self.document_facets.to_dict()

        segment_count = self.segment_count

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "corpusSize": corpus_size,
                "documentCount": document_count,
                "documentFacets": document_facets,
                "segmentCount": segment_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.document_facets import DocumentFacets

        d = dict(src_dict)
        corpus_size = d.pop("corpusSize")

        document_count = d.pop("documentCount")

        document_facets = DocumentFacets.from_dict(d.pop("documentFacets"))

        segment_count = d.pop("segmentCount")

        corpus_metrics = cls(
            corpus_size=corpus_size,
            document_count=document_count,
            document_facets=document_facets,
            segment_count=segment_count,
        )

        return corpus_metrics

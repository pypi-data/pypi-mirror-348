from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.metadata_count import MetadataCount


T = TypeVar("T", bound="DocumentFacets")


@_attrs_define
class DocumentFacets:
    """
    Attributes:
        facets (list['MetadataCount']):
        metadata (str):
    """

    facets: list["MetadataCount"]
    metadata: str

    def to_dict(self) -> dict[str, Any]:
        facets = []
        for facets_item_data in self.facets:
            facets_item = facets_item_data.to_dict()
            facets.append(facets_item)

        metadata = self.metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "facets": facets,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata_count import MetadataCount

        d = dict(src_dict)
        facets = []
        _facets = d.pop("facets")
        for facets_item_data in _facets:
            facets_item = MetadataCount.from_dict(facets_item_data)

            facets.append(facets_item)

        metadata = d.pop("metadata")

        document_facets = cls(
            facets=facets,
            metadata=metadata,
        )

        return document_facets

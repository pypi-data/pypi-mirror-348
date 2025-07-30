from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.doc_annotation import DocAnnotation
    from ..models.doc_category import DocCategory
    from ..models.segment_metadata import SegmentMetadata


T = TypeVar("T", bound="Segment")


@_attrs_define
class Segment:
    """
    Attributes:
        document_identifier (str):
        document_title (str):
        end (int):
        identifier (str):
        start (int):
        text (str):
        annotations (Union[Unset, list['DocAnnotation']]):
        categories (Union[Unset, list['DocCategory']]):
        created_by (Union[Unset, str]): User having created the segment
        created_date (Union[Unset, str]): Creation date
        metadata (Union[Unset, SegmentMetadata]):
        modified_date (Union[Unset, str]): Last modification date
        shift (Union[Unset, int]):
    """

    document_identifier: str
    document_title: str
    end: int
    identifier: str
    start: int
    text: str
    annotations: Union[Unset, list["DocAnnotation"]] = UNSET
    categories: Union[Unset, list["DocCategory"]] = UNSET
    created_by: Union[Unset, str] = UNSET
    created_date: Union[Unset, str] = UNSET
    metadata: Union[Unset, "SegmentMetadata"] = UNSET
    modified_date: Union[Unset, str] = UNSET
    shift: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        document_identifier = self.document_identifier

        document_title = self.document_title

        end = self.end

        identifier = self.identifier

        start = self.start

        text = self.text

        annotations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = []
            for annotations_item_data in self.annotations:
                annotations_item = annotations_item_data.to_dict()
                annotations.append(annotations_item)

        categories: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()
                categories.append(categories_item)

        created_by = self.created_by

        created_date = self.created_date

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        modified_date = self.modified_date

        shift = self.shift

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "documentIdentifier": document_identifier,
                "documentTitle": document_title,
                "end": end,
                "identifier": identifier,
                "start": start,
                "text": text,
            }
        )
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if categories is not UNSET:
            field_dict["categories"] = categories
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if modified_date is not UNSET:
            field_dict["modifiedDate"] = modified_date
        if shift is not UNSET:
            field_dict["shift"] = shift

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.doc_annotation import DocAnnotation
        from ..models.doc_category import DocCategory
        from ..models.segment_metadata import SegmentMetadata

        d = dict(src_dict)
        document_identifier = d.pop("documentIdentifier")

        document_title = d.pop("documentTitle")

        end = d.pop("end")

        identifier = d.pop("identifier")

        start = d.pop("start")

        text = d.pop("text")

        annotations = []
        _annotations = d.pop("annotations", UNSET)
        for annotations_item_data in _annotations or []:
            annotations_item = DocAnnotation.from_dict(annotations_item_data)

            annotations.append(annotations_item)

        categories = []
        _categories = d.pop("categories", UNSET)
        for categories_item_data in _categories or []:
            categories_item = DocCategory.from_dict(categories_item_data)

            categories.append(categories_item)

        created_by = d.pop("createdBy", UNSET)

        created_date = d.pop("createdDate", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, SegmentMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = SegmentMetadata.from_dict(_metadata)

        modified_date = d.pop("modifiedDate", UNSET)

        shift = d.pop("shift", UNSET)

        segment = cls(
            document_identifier=document_identifier,
            document_title=document_title,
            end=end,
            identifier=identifier,
            start=start,
            text=text,
            annotations=annotations,
            categories=categories,
            created_by=created_by,
            created_date=created_date,
            metadata=metadata,
            modified_date=modified_date,
            shift=shift,
        )

        return segment

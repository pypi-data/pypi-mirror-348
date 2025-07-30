from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.imported_doc_annotation_creation_mode import ImportedDocAnnotationCreationMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_term import AnnotationTerm
    from ..models.imported_doc_annotation_properties import ImportedDocAnnotationProperties


T = TypeVar("T", bound="ImportedDocAnnotation")


@attr.s(auto_attribs=True)
class ImportedDocAnnotation:
    """
    Attributes:
        end (int): End offset in document
        start (int): Start offset in document
        text (str): Covered text
        creation_mode (Union[Unset, ImportedDocAnnotationCreationMode]): Creation mode
        label (Union[Unset, str]): Human-friendly label
        label_id (Union[Unset, str]): External label identifier
        label_name (Union[Unset, str]): Label name
        properties (Union[Unset, ImportedDocAnnotationProperties]): Additional properties
        score (Union[Unset, float]): Score of the annotation
        status (Union[Unset, str]): Status
        terms (Union[Unset, List['AnnotationTerm']]):
    """

    end: int
    start: int
    text: str
    creation_mode: Union[Unset, ImportedDocAnnotationCreationMode] = UNSET
    label: Union[Unset, str] = UNSET
    label_id: Union[Unset, str] = UNSET
    label_name: Union[Unset, str] = UNSET
    properties: Union[Unset, "ImportedDocAnnotationProperties"] = UNSET
    score: Union[Unset, float] = UNSET
    status: Union[Unset, str] = UNSET
    terms: Union[Unset, List["AnnotationTerm"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        end = self.end
        start = self.start
        text = self.text
        creation_mode: Union[Unset, str] = UNSET
        if not isinstance(self.creation_mode, Unset):
            creation_mode = self.creation_mode.value

        label = self.label
        label_id = self.label_id
        label_name = self.label_name
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        score = self.score
        status = self.status
        terms: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.terms, Unset):
            terms = []
            for terms_item_data in self.terms:
                terms_item = terms_item_data.to_dict()

                terms.append(terms_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "end": end,
                "start": start,
                "text": text,
            }
        )
        if creation_mode is not UNSET:
            field_dict["creationMode"] = creation_mode
        if label is not UNSET:
            field_dict["label"] = label
        if label_id is not UNSET:
            field_dict["labelId"] = label_id
        if label_name is not UNSET:
            field_dict["labelName"] = label_name
        if properties is not UNSET:
            field_dict["properties"] = properties
        if score is not UNSET:
            field_dict["score"] = score
        if status is not UNSET:
            field_dict["status"] = status
        if terms is not UNSET:
            field_dict["terms"] = terms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.annotation_term import AnnotationTerm
        from ..models.imported_doc_annotation_properties import ImportedDocAnnotationProperties

        d = src_dict.copy()
        end = d.pop("end")

        start = d.pop("start")

        text = d.pop("text")

        _creation_mode = d.pop("creationMode", UNSET)
        creation_mode: Union[Unset, ImportedDocAnnotationCreationMode]
        if isinstance(_creation_mode, Unset):
            creation_mode = UNSET
        else:
            creation_mode = ImportedDocAnnotationCreationMode(_creation_mode)

        label = d.pop("label", UNSET)

        label_id = d.pop("labelId", UNSET)

        label_name = d.pop("labelName", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, ImportedDocAnnotationProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = ImportedDocAnnotationProperties.from_dict(_properties)

        score = d.pop("score", UNSET)

        status = d.pop("status", UNSET)

        terms = []
        _terms = d.pop("terms", UNSET)
        for terms_item_data in _terms or []:
            terms_item = AnnotationTerm.from_dict(terms_item_data)

            terms.append(terms_item)

        imported_doc_annotation = cls(
            end=end,
            start=start,
            text=text,
            creation_mode=creation_mode,
            label=label,
            label_id=label_id,
            label_name=label_name,
            properties=properties,
            score=score,
            status=status,
            terms=terms,
        )

        return imported_doc_annotation

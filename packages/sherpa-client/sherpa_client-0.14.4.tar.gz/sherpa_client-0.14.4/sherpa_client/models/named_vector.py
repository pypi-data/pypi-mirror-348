from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.named_vector_creation_mode import NamedVectorCreationMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_term import AnnotationTerm
    from ..models.named_vector_properties import NamedVectorProperties


T = TypeVar("T", bound="NamedVector")


@attr.s(auto_attribs=True)
class NamedVector:
    """A float vector

    Attributes:
        end (int): End offset in document
        name (str): Name
        start (int): Start offset in document
        text (str): Covered text
        creation_mode (Union[Unset, NamedVectorCreationMode]): Creation mode
        properties (Union[Unset, NamedVectorProperties]): Additional properties
        score (Union[Unset, float]): Score of the annotation
        terms (Union[Unset, List['AnnotationTerm']]):
    """

    end: int
    name: str
    start: int
    text: str
    creation_mode: Union[Unset, NamedVectorCreationMode] = UNSET
    properties: Union[Unset, "NamedVectorProperties"] = UNSET
    score: Union[Unset, float] = UNSET
    terms: Union[Unset, List["AnnotationTerm"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        end = self.end
        name = self.name
        start = self.start
        text = self.text
        creation_mode: Union[Unset, str] = UNSET
        if not isinstance(self.creation_mode, Unset):
            creation_mode = self.creation_mode.value

        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        score = self.score
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
                "name": name,
                "start": start,
                "text": text,
            }
        )
        if creation_mode is not UNSET:
            field_dict["creationMode"] = creation_mode
        if properties is not UNSET:
            field_dict["properties"] = properties
        if score is not UNSET:
            field_dict["score"] = score
        if terms is not UNSET:
            field_dict["terms"] = terms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.annotation_term import AnnotationTerm
        from ..models.named_vector_properties import NamedVectorProperties

        d = src_dict.copy()
        end = d.pop("end")

        name = d.pop("name")

        start = d.pop("start")

        text = d.pop("text")

        _creation_mode = d.pop("creationMode", UNSET)
        creation_mode: Union[Unset, NamedVectorCreationMode]
        if isinstance(_creation_mode, Unset):
            creation_mode = UNSET
        else:
            creation_mode = NamedVectorCreationMode(_creation_mode)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, NamedVectorProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = NamedVectorProperties.from_dict(_properties)

        score = d.pop("score", UNSET)

        terms = []
        _terms = d.pop("terms", UNSET)
        for terms_item_data in _terms or []:
            terms_item = AnnotationTerm.from_dict(terms_item_data)

            terms.append(terms_item)

        named_vector = cls(
            end=end,
            name=name,
            start=start,
            text=text,
            creation_mode=creation_mode,
            properties=properties,
            score=score,
            terms=terms,
        )

        return named_vector

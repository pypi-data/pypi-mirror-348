from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..models.imported_doc_category_creation_mode import ImportedDocCategoryCreationMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.imported_doc_category_properties import ImportedDocCategoryProperties


T = TypeVar("T", bound="ImportedDocCategory")


@attr.s(auto_attribs=True)
class ImportedDocCategory:
    """
    Attributes:
        creation_mode (Union[Unset, ImportedDocCategoryCreationMode]): Creation mode
        label (Union[Unset, str]): Human-friendly label
        label_id (Union[Unset, str]): External label identifier
        label_name (Union[Unset, str]): Label name
        properties (Union[Unset, ImportedDocCategoryProperties]): Additional properties
        score (Union[Unset, float]): Score of the category
        status (Union[Unset, str]): Status
    """

    creation_mode: Union[Unset, ImportedDocCategoryCreationMode] = UNSET
    label: Union[Unset, str] = UNSET
    label_id: Union[Unset, str] = UNSET
    label_name: Union[Unset, str] = UNSET
    properties: Union[Unset, "ImportedDocCategoryProperties"] = UNSET
    score: Union[Unset, float] = UNSET
    status: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
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

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.imported_doc_category_properties import ImportedDocCategoryProperties

        d = src_dict.copy()
        _creation_mode = d.pop("creationMode", UNSET)
        creation_mode: Union[Unset, ImportedDocCategoryCreationMode]
        if isinstance(_creation_mode, Unset):
            creation_mode = UNSET
        else:
            creation_mode = ImportedDocCategoryCreationMode(_creation_mode)

        label = d.pop("label", UNSET)

        label_id = d.pop("labelId", UNSET)

        label_name = d.pop("labelName", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, ImportedDocCategoryProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = ImportedDocCategoryProperties.from_dict(_properties)

        score = d.pop("score", UNSET)

        status = d.pop("status", UNSET)

        imported_doc_category = cls(
            creation_mode=creation_mode,
            label=label,
            label_id=label_id,
            label_name=label_name,
            properties=properties,
            score=score,
            status=status,
        )

        return imported_doc_category

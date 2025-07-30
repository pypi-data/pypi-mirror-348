from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..models.doc_category_creation_mode import DocCategoryCreationMode
from ..models.doc_category_status import DocCategoryStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.doc_category_properties import DocCategoryProperties


T = TypeVar("T", bound="DocCategory")


@attr.s(auto_attribs=True)
class DocCategory:
    """A document category

    Attributes:
        label_name (str): The label name
        created_by (Union[Unset, str]): User having created the category
        created_date (Union[Unset, str]): Creation date
        creation_mode (Union[Unset, DocCategoryCreationMode]): Creation mode
        identifier (Union[Unset, str]): Category identifier
        modified_date (Union[Unset, str]): Last modification date
        properties (Union[Unset, DocCategoryProperties]): Additional properties
        score (Union[Unset, float]): Score of the category
        status (Union[Unset, DocCategoryStatus]): Status of the category
    """

    label_name: str
    created_by: Union[Unset, str] = UNSET
    created_date: Union[Unset, str] = UNSET
    creation_mode: Union[Unset, DocCategoryCreationMode] = UNSET
    identifier: Union[Unset, str] = UNSET
    modified_date: Union[Unset, str] = UNSET
    properties: Union[Unset, "DocCategoryProperties"] = UNSET
    score: Union[Unset, float] = UNSET
    status: Union[Unset, DocCategoryStatus] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label_name = self.label_name
        created_by = self.created_by
        created_date = self.created_date
        creation_mode: Union[Unset, str] = UNSET
        if not isinstance(self.creation_mode, Unset):
            creation_mode = self.creation_mode.value

        identifier = self.identifier
        modified_date = self.modified_date
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        score = self.score
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "labelName": label_name,
            }
        )
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if creation_mode is not UNSET:
            field_dict["creationMode"] = creation_mode
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if modified_date is not UNSET:
            field_dict["modifiedDate"] = modified_date
        if properties is not UNSET:
            field_dict["properties"] = properties
        if score is not UNSET:
            field_dict["score"] = score
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.doc_category_properties import DocCategoryProperties

        d = src_dict.copy()
        label_name = d.pop("labelName")

        created_by = d.pop("createdBy", UNSET)

        created_date = d.pop("createdDate", UNSET)

        _creation_mode = d.pop("creationMode", UNSET)
        creation_mode: Union[Unset, DocCategoryCreationMode]
        if isinstance(_creation_mode, Unset):
            creation_mode = UNSET
        else:
            creation_mode = DocCategoryCreationMode(_creation_mode)

        identifier = d.pop("identifier", UNSET)

        modified_date = d.pop("modifiedDate", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, DocCategoryProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = DocCategoryProperties.from_dict(_properties)

        score = d.pop("score", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, DocCategoryStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = DocCategoryStatus(_status)

        doc_category = cls(
            label_name=label_name,
            created_by=created_by,
            created_date=created_date,
            creation_mode=creation_mode,
            identifier=identifier,
            modified_date=modified_date,
            properties=properties,
            score=score,
            status=status,
        )

        return doc_category

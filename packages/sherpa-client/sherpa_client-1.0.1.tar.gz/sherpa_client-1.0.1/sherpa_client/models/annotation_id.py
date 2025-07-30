from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AnnotationId")


@_attrs_define
class AnnotationId:
    """Annotation creation response

    Attributes:
        identifier (str): Identifier of the new annotation
    """

    identifier: str

    def to_dict(self) -> dict[str, Any]:
        identifier = self.identifier

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "identifier": identifier,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        identifier = d.pop("identifier")

        annotation_id = cls(
            identifier=identifier,
        )

        return annotation_id

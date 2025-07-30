from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.annotation_patch_status import AnnotationPatchStatus

T = TypeVar("T", bound="AnnotationPatch")


@_attrs_define
class AnnotationPatch:
    """
    Attributes:
        status (AnnotationPatchStatus): Status of the category
    """

    status: AnnotationPatchStatus

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = AnnotationPatchStatus(d.pop("status"))

        annotation_patch = cls(
            status=status,
        )

        return annotation_patch

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.category_patch_status import CategoryPatchStatus

T = TypeVar("T", bound="CategoryPatch")


@_attrs_define
class CategoryPatch:
    """
    Attributes:
        status (CategoryPatchStatus): Status of the category
    """

    status: CategoryPatchStatus

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
        status = CategoryPatchStatus(d.pop("status"))

        category_patch = cls(
            status=status,
        )

        return category_patch

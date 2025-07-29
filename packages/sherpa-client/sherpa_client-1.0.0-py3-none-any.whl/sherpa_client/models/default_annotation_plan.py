from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_plan import AnnotationPlan


T = TypeVar("T", bound="DefaultAnnotationPlan")


@_attrs_define
class DefaultAnnotationPlan:
    """
    Attributes:
        parameters (AnnotationPlan):
        tags (Union[Unset, list[str]]):
    """

    parameters: "AnnotationPlan"
    tags: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        parameters = self.parameters.to_dict()

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "parameters": parameters,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.annotation_plan import AnnotationPlan

        d = dict(src_dict)
        parameters = AnnotationPlan.from_dict(d.pop("parameters"))

        tags = cast(list[str], d.pop("tags", UNSET))

        default_annotation_plan = cls(
            parameters=parameters,
            tags=tags,
        )

        return default_annotation_plan

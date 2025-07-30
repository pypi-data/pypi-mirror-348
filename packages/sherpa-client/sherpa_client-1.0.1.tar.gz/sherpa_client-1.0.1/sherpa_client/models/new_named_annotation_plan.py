from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_plan import AnnotationPlan


T = TypeVar("T", bound="NewNamedAnnotationPlan")


@_attrs_define
class NewNamedAnnotationPlan:
    """
    Attributes:
        label (str):
        parameters (AnnotationPlan):
        tags (Union[Unset, list[str]]):
    """

    label: str
    parameters: "AnnotationPlan"
    tags: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        parameters = self.parameters.to_dict()

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
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
        label = d.pop("label")

        parameters = AnnotationPlan.from_dict(d.pop("parameters"))

        tags = cast(list[str], d.pop("tags", UNSET))

        new_named_annotation_plan = cls(
            label=label,
            parameters=parameters,
            tags=tags,
        )

        return new_named_annotation_plan

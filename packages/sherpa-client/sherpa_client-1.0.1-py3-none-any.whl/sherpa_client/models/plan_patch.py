from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_plan import AnnotationPlan


T = TypeVar("T", bound="PlanPatch")


@_attrs_define
class PlanPatch:
    """
    Attributes:
        favorite (Union[Unset, bool]):
        label (Union[Unset, str]):
        parameters (Union[Unset, AnnotationPlan]):
        tags (Union[Unset, list[str]]):
    """

    favorite: Union[Unset, bool] = UNSET
    label: Union[Unset, str] = UNSET
    parameters: Union[Unset, "AnnotationPlan"] = UNSET
    tags: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        favorite = self.favorite

        label = self.label

        parameters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if favorite is not UNSET:
            field_dict["favorite"] = favorite
        if label is not UNSET:
            field_dict["label"] = label
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.annotation_plan import AnnotationPlan

        d = dict(src_dict)
        favorite = d.pop("favorite", UNSET)

        label = d.pop("label", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, AnnotationPlan]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = AnnotationPlan.from_dict(_parameters)

        tags = cast(list[str], d.pop("tags", UNSET))

        plan_patch = cls(
            favorite=favorite,
            label=label,
            parameters=parameters,
            tags=tags,
        )

        return plan_patch

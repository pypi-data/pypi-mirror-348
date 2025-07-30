from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_plan import AnnotationPlan


T = TypeVar("T", bound="DefaultAnnotationPlan")


@attr.s(auto_attribs=True)
class DefaultAnnotationPlan:
    """
    Attributes:
        parameters (AnnotationPlan):
        tags (Union[Unset, List[str]]):
    """

    parameters: "AnnotationPlan"
    tags: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        parameters = self.parameters.to_dict()

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "parameters": parameters,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.annotation_plan import AnnotationPlan

        d = src_dict.copy()
        parameters = AnnotationPlan.from_dict(d.pop("parameters"))

        tags = cast(List[str], d.pop("tags", UNSET))

        default_annotation_plan = cls(
            parameters=parameters,
            tags=tags,
        )

        return default_annotation_plan

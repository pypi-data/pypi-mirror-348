from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.apply_to import ApplyTo
    from ..models.with_segmenter_condition import WithSegmenterCondition
    from ..models.with_segmenter_parameters import WithSegmenterParameters


T = TypeVar("T", bound="WithSegmenter")


@attr.s(auto_attribs=True)
class WithSegmenter:
    """
    Attributes:
        segmenter (str):
        apply_to (Union[Unset, ApplyTo]):
        condition (Union[Unset, WithSegmenterCondition]):
        disabled (Union[Unset, bool]):
        parameters (Union[Unset, WithSegmenterParameters]):
        project_name (Union[Unset, str]):
    """

    segmenter: str
    apply_to: Union[Unset, "ApplyTo"] = UNSET
    condition: Union[Unset, "WithSegmenterCondition"] = UNSET
    disabled: Union[Unset, bool] = UNSET
    parameters: Union[Unset, "WithSegmenterParameters"] = UNSET
    project_name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        segmenter = self.segmenter
        apply_to: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.apply_to, Unset):
            apply_to = self.apply_to.to_dict()

        condition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.condition, Unset):
            condition = self.condition.to_dict()

        disabled = self.disabled
        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        project_name = self.project_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "segmenter": segmenter,
            }
        )
        if apply_to is not UNSET:
            field_dict["applyTo"] = apply_to
        if condition is not UNSET:
            field_dict["condition"] = condition
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if project_name is not UNSET:
            field_dict["projectName"] = project_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.apply_to import ApplyTo
        from ..models.with_segmenter_condition import WithSegmenterCondition
        from ..models.with_segmenter_parameters import WithSegmenterParameters

        d = src_dict.copy()
        segmenter = d.pop("segmenter")

        _apply_to = d.pop("applyTo", UNSET)
        apply_to: Union[Unset, ApplyTo]
        if isinstance(_apply_to, Unset):
            apply_to = UNSET
        else:
            apply_to = ApplyTo.from_dict(_apply_to)

        _condition = d.pop("condition", UNSET)
        condition: Union[Unset, WithSegmenterCondition]
        if isinstance(_condition, Unset):
            condition = UNSET
        else:
            condition = WithSegmenterCondition.from_dict(_condition)

        disabled = d.pop("disabled", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, WithSegmenterParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = WithSegmenterParameters.from_dict(_parameters)

        project_name = d.pop("projectName", UNSET)

        with_segmenter = cls(
            segmenter=segmenter,
            apply_to=apply_to,
            condition=condition,
            disabled=disabled,
            parameters=parameters,
            project_name=project_name,
        )

        return with_segmenter

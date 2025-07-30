from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.apply_to import ApplyTo
    from ..models.with_annotator_condition import WithAnnotatorCondition
    from ..models.with_annotator_parameters import WithAnnotatorParameters


T = TypeVar("T", bound="WithAnnotator")


@_attrs_define
class WithAnnotator:
    """
    Attributes:
        annotator (str):
        apply_to (Union[Unset, ApplyTo]):
        condition (Union[Unset, WithAnnotatorCondition]):
        disabled (Union[Unset, bool]):
        parameters (Union[Unset, WithAnnotatorParameters]):
        project_name (Union[Unset, str]):
    """

    annotator: str
    apply_to: Union[Unset, "ApplyTo"] = UNSET
    condition: Union[Unset, "WithAnnotatorCondition"] = UNSET
    disabled: Union[Unset, bool] = UNSET
    parameters: Union[Unset, "WithAnnotatorParameters"] = UNSET
    project_name: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        annotator = self.annotator

        apply_to: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.apply_to, Unset):
            apply_to = self.apply_to.to_dict()

        condition: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.condition, Unset):
            condition = self.condition.to_dict()

        disabled = self.disabled

        parameters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        project_name = self.project_name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "annotator": annotator,
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.apply_to import ApplyTo
        from ..models.with_annotator_condition import WithAnnotatorCondition
        from ..models.with_annotator_parameters import WithAnnotatorParameters

        d = dict(src_dict)
        annotator = d.pop("annotator")

        _apply_to = d.pop("applyTo", UNSET)
        apply_to: Union[Unset, ApplyTo]
        if isinstance(_apply_to, Unset):
            apply_to = UNSET
        else:
            apply_to = ApplyTo.from_dict(_apply_to)

        _condition = d.pop("condition", UNSET)
        condition: Union[Unset, WithAnnotatorCondition]
        if isinstance(_condition, Unset):
            condition = UNSET
        else:
            condition = WithAnnotatorCondition.from_dict(_condition)

        disabled = d.pop("disabled", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, WithAnnotatorParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = WithAnnotatorParameters.from_dict(_parameters)

        project_name = d.pop("projectName", UNSET)

        with_annotator = cls(
            annotator=annotator,
            apply_to=apply_to,
            condition=condition,
            disabled=disabled,
            parameters=parameters,
            project_name=project_name,
        )

        return with_annotator

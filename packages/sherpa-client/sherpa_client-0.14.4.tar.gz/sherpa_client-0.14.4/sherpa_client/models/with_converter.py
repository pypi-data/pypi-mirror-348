from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.apply_to import ApplyTo
    from ..models.with_converter_condition import WithConverterCondition
    from ..models.with_converter_parameters import WithConverterParameters


T = TypeVar("T", bound="WithConverter")


@attr.s(auto_attribs=True)
class WithConverter:
    """
    Attributes:
        converter (str):
        apply_to (Union[Unset, ApplyTo]):
        condition (Union[Unset, WithConverterCondition]):
        disabled (Union[Unset, bool]):
        parameters (Union[Unset, WithConverterParameters]):
        project_name (Union[Unset, str]):
    """

    converter: str
    apply_to: Union[Unset, "ApplyTo"] = UNSET
    condition: Union[Unset, "WithConverterCondition"] = UNSET
    disabled: Union[Unset, bool] = UNSET
    parameters: Union[Unset, "WithConverterParameters"] = UNSET
    project_name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        converter = self.converter
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
                "converter": converter,
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
        from ..models.with_converter_condition import WithConverterCondition
        from ..models.with_converter_parameters import WithConverterParameters

        d = src_dict.copy()
        converter = d.pop("converter")

        _apply_to = d.pop("applyTo", UNSET)
        apply_to: Union[Unset, ApplyTo]
        if isinstance(_apply_to, Unset):
            apply_to = UNSET
        else:
            apply_to = ApplyTo.from_dict(_apply_to)

        _condition = d.pop("condition", UNSET)
        condition: Union[Unset, WithConverterCondition]
        if isinstance(_condition, Unset):
            condition = UNSET
        else:
            condition = WithConverterCondition.from_dict(_condition)

        disabled = d.pop("disabled", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, WithConverterParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = WithConverterParameters.from_dict(_parameters)

        project_name = d.pop("projectName", UNSET)

        with_converter = cls(
            converter=converter,
            apply_to=apply_to,
            condition=condition,
            disabled=disabled,
            parameters=parameters,
            project_name=project_name,
        )

        return with_converter

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.with_processor_condition import WithProcessorCondition
    from ..models.with_processor_parameters import WithProcessorParameters


T = TypeVar("T", bound="WithProcessor")


@_attrs_define
class WithProcessor:
    """
    Attributes:
        processor (str):
        condition (Union[Unset, WithProcessorCondition]):
        disabled (Union[Unset, bool]):
        parameters (Union[Unset, WithProcessorParameters]):
    """

    processor: str
    condition: Union[Unset, "WithProcessorCondition"] = UNSET
    disabled: Union[Unset, bool] = UNSET
    parameters: Union[Unset, "WithProcessorParameters"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        processor = self.processor

        condition: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.condition, Unset):
            condition = self.condition.to_dict()

        disabled = self.disabled

        parameters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "processor": processor,
            }
        )
        if condition is not UNSET:
            field_dict["condition"] = condition
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.with_processor_condition import WithProcessorCondition
        from ..models.with_processor_parameters import WithProcessorParameters

        d = dict(src_dict)
        processor = d.pop("processor")

        _condition = d.pop("condition", UNSET)
        condition: Union[Unset, WithProcessorCondition]
        if isinstance(_condition, Unset):
            condition = UNSET
        else:
            condition = WithProcessorCondition.from_dict(_condition)

        disabled = d.pop("disabled", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, WithProcessorParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = WithProcessorParameters.from_dict(_parameters)

        with_processor = cls(
            processor=processor,
            condition=condition,
            disabled=disabled,
            parameters=parameters,
        )

        return with_processor

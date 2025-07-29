from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.converter_parameters import ConverterParameters


T = TypeVar("T", bound="Converter")


@_attrs_define
class Converter:
    """
    Attributes:
        name (str): Name of the converter (e.g. tika)
        parameters (Union[Unset, ConverterParameters]): Optional conversion parameters
    """

    name: str
    parameters: Union[Unset, "ConverterParameters"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        parameters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.converter_parameters import ConverterParameters

        d = dict(src_dict)
        name = d.pop("name")

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, ConverterParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = ConverterParameters.from_dict(_parameters)

        converter = cls(
            name=name,
            parameters=parameters,
        )

        return converter

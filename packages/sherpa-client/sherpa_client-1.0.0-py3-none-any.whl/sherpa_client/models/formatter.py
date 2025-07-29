from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.formatter_parameters import FormatterParameters


T = TypeVar("T", bound="Formatter")


@_attrs_define
class Formatter:
    """
    Attributes:
        name (str): Name of the formatter (e.g. tabular)
        parameters (Union[Unset, FormatterParameters]): Optional formatting parameters
    """

    name: str
    parameters: Union[Unset, "FormatterParameters"] = UNSET

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
        from ..models.formatter_parameters import FormatterParameters

        d = dict(src_dict)
        name = d.pop("name")

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, FormatterParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = FormatterParameters.from_dict(_parameters)

        formatter = cls(
            name=name,
            parameters=parameters,
        )

        return formatter

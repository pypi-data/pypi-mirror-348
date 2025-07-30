from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.term_importer_spec_parameters import TermImporterSpecParameters


T = TypeVar("T", bound="TermImporterSpec")


@_attrs_define
class TermImporterSpec:
    """
    Attributes:
        format_ (str):
        parameters (TermImporterSpecParameters):
    """

    format_: str
    parameters: "TermImporterSpecParameters"

    def to_dict(self) -> dict[str, Any]:
        format_ = self.format_

        parameters = self.parameters.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "format": format_,
                "parameters": parameters,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.term_importer_spec_parameters import TermImporterSpecParameters

        d = dict(src_dict)
        format_ = d.pop("format")

        parameters = TermImporterSpecParameters.from_dict(d.pop("parameters"))

        term_importer_spec = cls(
            format_=format_,
            parameters=parameters,
        )

        return term_importer_spec

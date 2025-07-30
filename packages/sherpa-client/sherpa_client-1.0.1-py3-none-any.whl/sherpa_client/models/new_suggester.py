from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_suggester_parameters import NewSuggesterParameters


T = TypeVar("T", bound="NewSuggester")


@_attrs_define
class NewSuggester:
    """
    Attributes:
        engine (str):
        label (str):
        parameters (NewSuggesterParameters):
        tags (Union[Unset, list[str]]):
    """

    engine: str
    label: str
    parameters: "NewSuggesterParameters"
    tags: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        engine = self.engine

        label = self.label

        parameters = self.parameters.to_dict()

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "engine": engine,
                "label": label,
                "parameters": parameters,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.new_suggester_parameters import NewSuggesterParameters

        d = dict(src_dict)
        engine = d.pop("engine")

        label = d.pop("label")

        parameters = NewSuggesterParameters.from_dict(d.pop("parameters"))

        tags = cast(list[str], d.pop("tags", UNSET))

        new_suggester = cls(
            engine=engine,
            label=label,
            parameters=parameters,
            tags=tags,
        )

        return new_suggester

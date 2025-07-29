from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.suggester_patch_parameters import SuggesterPatchParameters


T = TypeVar("T", bound="SuggesterPatch")


@_attrs_define
class SuggesterPatch:
    """
    Attributes:
        label (Union[Unset, str]):
        parameters (Union[Unset, SuggesterPatchParameters]):
        tags (Union[Unset, list[str]]):
    """

    label: Union[Unset, str] = UNSET
    parameters: Union[Unset, "SuggesterPatchParameters"] = UNSET
    tags: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        parameters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.suggester_patch_parameters import SuggesterPatchParameters

        d = dict(src_dict)
        label = d.pop("label", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, SuggesterPatchParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = SuggesterPatchParameters.from_dict(_parameters)

        tags = cast(list[str], d.pop("tags", UNSET))

        suggester_patch = cls(
            label=label,
            parameters=parameters,
            tags=tags,
        )

        return suggester_patch

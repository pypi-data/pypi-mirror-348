from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PartialLexicon")


@_attrs_define
class PartialLexicon:
    """
    Attributes:
        label (str):
        color (Union[Unset, str]):
        name (Union[Unset, str]):
    """

    label: str
    color: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        color = self.color

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
            }
        )
        if color is not UNSET:
            field_dict["color"] = color
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        color = d.pop("color", UNSET)

        name = d.pop("name", UNSET)

        partial_lexicon = cls(
            label=label,
            color=color,
            name=name,
        )

        return partial_lexicon

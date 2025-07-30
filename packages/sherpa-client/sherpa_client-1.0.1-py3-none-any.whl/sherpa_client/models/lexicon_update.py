from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="LexiconUpdate")


@_attrs_define
class LexiconUpdate:
    """
    Attributes:
        color (Union[Unset, str]):
        label (Union[Unset, str]):
    """

    color: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        color = self.color

        label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        color = d.pop("color", UNSET)

        label = d.pop("label", UNSET)

        lexicon_update = cls(
            color=color,
            label=label,
        )

        return lexicon_update

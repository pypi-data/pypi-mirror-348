from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PartialLabel")


@_attrs_define
class PartialLabel:
    """
    Attributes:
        color (Union[Unset, str]):
        guideline (Union[Unset, str]):
        identifier (Union[Unset, str]):
        label (Union[Unset, str]):
        label_set_name (Union[Unset, str]):
        name (Union[Unset, str]):
    """

    color: Union[Unset, str] = UNSET
    guideline: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    label_set_name: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        color = self.color

        guideline = self.guideline

        identifier = self.identifier

        label = self.label

        label_set_name = self.label_set_name

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if guideline is not UNSET:
            field_dict["guideline"] = guideline
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if label is not UNSET:
            field_dict["label"] = label
        if label_set_name is not UNSET:
            field_dict["labelSetName"] = label_set_name
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        color = d.pop("color", UNSET)

        guideline = d.pop("guideline", UNSET)

        identifier = d.pop("identifier", UNSET)

        label = d.pop("label", UNSET)

        label_set_name = d.pop("labelSetName", UNSET)

        name = d.pop("name", UNSET)

        partial_label = cls(
            color=color,
            guideline=guideline,
            identifier=identifier,
            label=label,
            label_set_name=label_set_name,
            name=name,
        )

        return partial_label

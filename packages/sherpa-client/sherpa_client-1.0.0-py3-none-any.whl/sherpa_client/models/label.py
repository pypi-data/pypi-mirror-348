from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Label")


@_attrs_define
class Label:
    """
    Attributes:
        color (str):
        label (str):
        name (str):
        count (Union[Unset, int]):
        guideline (Union[Unset, str]):
        identifier (Union[Unset, str]):
        label_set_name (Union[Unset, str]):
    """

    color: str
    label: str
    name: str
    count: Union[Unset, int] = UNSET
    guideline: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    label_set_name: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        color = self.color

        label = self.label

        name = self.name

        count = self.count

        guideline = self.guideline

        identifier = self.identifier

        label_set_name = self.label_set_name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "color": color,
                "label": label,
                "name": name,
            }
        )
        if count is not UNSET:
            field_dict["count"] = count
        if guideline is not UNSET:
            field_dict["guideline"] = guideline
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if label_set_name is not UNSET:
            field_dict["labelSetName"] = label_set_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        color = d.pop("color")

        label = d.pop("label")

        name = d.pop("name")

        count = d.pop("count", UNSET)

        guideline = d.pop("guideline", UNSET)

        identifier = d.pop("identifier", UNSET)

        label_set_name = d.pop("labelSetName", UNSET)

        label = cls(
            color=color,
            label=label,
            name=name,
            count=count,
            guideline=guideline,
            identifier=identifier,
            label_set_name=label_set_name,
        )

        return label

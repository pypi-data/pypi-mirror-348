from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="LabelSetUpdate")


@_attrs_define
class LabelSetUpdate:
    """
    Attributes:
        exclusive_classes (Union[Unset, bool]):
        guideline (Union[Unset, str]):
        label (Union[Unset, str]):
        nature (Union[Unset, str]):
        tags (Union[Unset, list[str]]):
    """

    exclusive_classes: Union[Unset, bool] = UNSET
    guideline: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    nature: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        exclusive_classes = self.exclusive_classes

        guideline = self.guideline

        label = self.label

        nature = self.nature

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if exclusive_classes is not UNSET:
            field_dict["exclusiveClasses"] = exclusive_classes
        if guideline is not UNSET:
            field_dict["guideline"] = guideline
        if label is not UNSET:
            field_dict["label"] = label
        if nature is not UNSET:
            field_dict["nature"] = nature
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        exclusive_classes = d.pop("exclusiveClasses", UNSET)

        guideline = d.pop("guideline", UNSET)

        label = d.pop("label", UNSET)

        nature = d.pop("nature", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        label_set_update = cls(
            exclusive_classes=exclusive_classes,
            guideline=guideline,
            label=label,
            nature=nature,
            tags=tags,
        )

        return label_set_update

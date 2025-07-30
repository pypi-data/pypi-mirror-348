from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ClassificationOptions")


@_attrs_define
class ClassificationOptions:
    """
    Attributes:
        exclusive_classes (Union[Unset, bool]):  Default: True.
    """

    exclusive_classes: Union[Unset, bool] = True

    def to_dict(self) -> dict[str, Any]:
        exclusive_classes = self.exclusive_classes

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if exclusive_classes is not UNSET:
            field_dict["exclusive_classes"] = exclusive_classes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        exclusive_classes = d.pop("exclusive_classes", UNSET)

        classification_options = cls(
            exclusive_classes=exclusive_classes,
        )

        return classification_options

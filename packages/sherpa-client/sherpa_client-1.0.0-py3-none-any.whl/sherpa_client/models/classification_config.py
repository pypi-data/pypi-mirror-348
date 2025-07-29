from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ClassificationConfig")


@_attrs_define
class ClassificationConfig:
    """
    Attributes:
        exclusive_classes (bool):
    """

    exclusive_classes: bool

    def to_dict(self) -> dict[str, Any]:
        exclusive_classes = self.exclusive_classes

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "exclusive_classes": exclusive_classes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        exclusive_classes = d.pop("exclusive_classes")

        classification_config = cls(
            exclusive_classes=exclusive_classes,
        )

        return classification_config

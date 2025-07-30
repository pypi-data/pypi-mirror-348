from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.label_count import LabelCount


T = TypeVar("T", bound="CategoriesFacets")


@_attrs_define
class CategoriesFacets:
    """
    Attributes:
        labels (list['LabelCount']):
    """

    labels: list["LabelCount"]

    def to_dict(self) -> dict[str, Any]:
        labels = []
        for labels_item_data in self.labels:
            labels_item = labels_item_data.to_dict()
            labels.append(labels_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "labels": labels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.label_count import LabelCount

        d = dict(src_dict)
        labels = []
        _labels = d.pop("labels")
        for labels_item_data in _labels:
            labels_item = LabelCount.from_dict(labels_item_data)

            labels.append(labels_item)

        categories_facets = cls(
            labels=labels,
        )

        return categories_facets

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.label_count import LabelCount
    from ..models.text_count import TextCount


T = TypeVar("T", bound="SuggestionFacets")


@_attrs_define
class SuggestionFacets:
    """
    Attributes:
        labels (list['LabelCount']):
        texts (list['TextCount']):
    """

    labels: list["LabelCount"]
    texts: list["TextCount"]

    def to_dict(self) -> dict[str, Any]:
        labels = []
        for labels_item_data in self.labels:
            labels_item = labels_item_data.to_dict()
            labels.append(labels_item)

        texts = []
        for texts_item_data in self.texts:
            texts_item = texts_item_data.to_dict()
            texts.append(texts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "labels": labels,
                "texts": texts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.label_count import LabelCount
        from ..models.text_count import TextCount

        d = dict(src_dict)
        labels = []
        _labels = d.pop("labels")
        for labels_item_data in _labels:
            labels_item = LabelCount.from_dict(labels_item_data)

            labels.append(labels_item)

        texts = []
        _texts = d.pop("texts")
        for texts_item_data in _texts:
            texts_item = TextCount.from_dict(texts_item_data)

            texts.append(texts_item)

        suggestion_facets = cls(
            labels=labels,
            texts=texts,
        )

        return suggestion_facets

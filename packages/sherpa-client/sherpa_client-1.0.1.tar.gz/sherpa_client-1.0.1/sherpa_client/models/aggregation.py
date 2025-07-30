from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.bucket import Bucket


T = TypeVar("T", bound="Aggregation")


@_attrs_define
class Aggregation:
    """
    Attributes:
        buckets (list['Bucket']):
        name (str):
    """

    buckets: list["Bucket"]
    name: str

    def to_dict(self) -> dict[str, Any]:
        buckets = []
        for buckets_item_data in self.buckets:
            buckets_item = buckets_item_data.to_dict()
            buckets.append(buckets_item)

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "buckets": buckets,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bucket import Bucket

        d = dict(src_dict)
        buckets = []
        _buckets = d.pop("buckets")
        for buckets_item_data in _buckets:
            buckets_item = Bucket.from_dict(buckets_item_data)

            buckets.append(buckets_item)

        name = d.pop("name")

        aggregation = cls(
            buckets=buckets,
            name=name,
        )

        return aggregation

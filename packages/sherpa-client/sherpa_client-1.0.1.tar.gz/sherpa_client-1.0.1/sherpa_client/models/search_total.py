from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.search_total_relation import SearchTotalRelation

T = TypeVar("T", bound="SearchTotal")


@_attrs_define
class SearchTotal:
    """
    Attributes:
        relation (SearchTotalRelation):
        value (int):
    """

    relation: SearchTotalRelation
    value: int

    def to_dict(self) -> dict[str, Any]:
        relation = self.relation.value

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "relation": relation,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        relation = SearchTotalRelation(d.pop("relation"))

        value = d.pop("value")

        search_total = cls(
            relation=relation,
            value=value,
        )

        return search_total

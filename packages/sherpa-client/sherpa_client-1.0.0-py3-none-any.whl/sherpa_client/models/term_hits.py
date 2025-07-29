from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_total import SearchTotal
    from ..models.term_hit import TermHit


T = TypeVar("T", bound="TermHits")


@_attrs_define
class TermHits:
    """
    Attributes:
        hits (list['TermHit']):
        total (SearchTotal):
        max_score (Union[Unset, float]):
    """

    hits: list["TermHit"]
    total: "SearchTotal"
    max_score: Union[Unset, float] = UNSET

    def to_dict(self) -> dict[str, Any]:
        hits = []
        for hits_item_data in self.hits:
            hits_item = hits_item_data.to_dict()
            hits.append(hits_item)

        total = self.total.to_dict()

        max_score = self.max_score

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "hits": hits,
                "total": total,
            }
        )
        if max_score is not UNSET:
            field_dict["max_score"] = max_score

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_total import SearchTotal
        from ..models.term_hit import TermHit

        d = dict(src_dict)
        hits = []
        _hits = d.pop("hits")
        for hits_item_data in _hits:
            hits_item = TermHit.from_dict(hits_item_data)

            hits.append(hits_item)

        total = SearchTotal.from_dict(d.pop("total"))

        max_score = d.pop("max_score", UNSET)

        term_hits = cls(
            hits=hits,
            total=total,
            max_score=max_score,
        )

        return term_hits

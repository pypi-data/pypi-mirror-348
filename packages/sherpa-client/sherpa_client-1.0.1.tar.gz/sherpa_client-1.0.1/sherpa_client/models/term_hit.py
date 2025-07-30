from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.term_hit_term import TermHitTerm


T = TypeVar("T", bound="TermHit")


@_attrs_define
class TermHit:
    """
    Attributes:
        score (float):
        term (TermHitTerm):
    """

    score: float
    term: "TermHitTerm"

    def to_dict(self) -> dict[str, Any]:
        score = self.score

        term = self.term.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "score": score,
                "term": term,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.term_hit_term import TermHitTerm

        d = dict(src_dict)
        score = d.pop("score")

        term = TermHitTerm.from_dict(d.pop("term"))

        term_hit = cls(
            score=score,
            term=term,
        )

        return term_hit

from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="QualityFigures")


@_attrs_define
class QualityFigures:
    """
    Attributes:
        support (int):
        ap (Union[Unset, float]):
        f1 (Union[Unset, float]):
        ndcg (Union[Unset, float]):
        precision (Union[Unset, float]):
        recall (Union[Unset, float]):
        roc_auc (Union[Unset, float]):
        rr (Union[Unset, float]):
    """

    support: int
    ap: Union[Unset, float] = UNSET
    f1: Union[Unset, float] = UNSET
    ndcg: Union[Unset, float] = UNSET
    precision: Union[Unset, float] = UNSET
    recall: Union[Unset, float] = UNSET
    roc_auc: Union[Unset, float] = UNSET
    rr: Union[Unset, float] = UNSET

    def to_dict(self) -> dict[str, Any]:
        support = self.support

        ap = self.ap

        f1 = self.f1

        ndcg = self.ndcg

        precision = self.precision

        recall = self.recall

        roc_auc = self.roc_auc

        rr = self.rr

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "support": support,
            }
        )
        if ap is not UNSET:
            field_dict["ap"] = ap
        if f1 is not UNSET:
            field_dict["f1"] = f1
        if ndcg is not UNSET:
            field_dict["ndcg"] = ndcg
        if precision is not UNSET:
            field_dict["precision"] = precision
        if recall is not UNSET:
            field_dict["recall"] = recall
        if roc_auc is not UNSET:
            field_dict["roc_auc"] = roc_auc
        if rr is not UNSET:
            field_dict["rr"] = rr

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        support = d.pop("support")

        ap = d.pop("ap", UNSET)

        f1 = d.pop("f1", UNSET)

        ndcg = d.pop("ndcg", UNSET)

        precision = d.pop("precision", UNSET)

        recall = d.pop("recall", UNSET)

        roc_auc = d.pop("roc_auc", UNSET)

        rr = d.pop("rr", UNSET)

        quality_figures = cls(
            support=support,
            ap=ap,
            f1=f1,
            ndcg=ndcg,
            precision=precision,
            recall=recall,
            roc_auc=roc_auc,
            rr=rr,
        )

        return quality_figures

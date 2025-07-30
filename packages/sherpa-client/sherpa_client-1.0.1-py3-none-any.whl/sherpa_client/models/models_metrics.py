from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_metrics import ModelMetrics


T = TypeVar("T", bound="ModelsMetrics")


@_attrs_define
class ModelsMetrics:
    """
    Attributes:
        history (list['ModelMetrics']):
        best (Union[Unset, ModelMetrics]):
        last (Union[Unset, ModelMetrics]):
    """

    history: list["ModelMetrics"]
    best: Union[Unset, "ModelMetrics"] = UNSET
    last: Union[Unset, "ModelMetrics"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        history = []
        for history_item_data in self.history:
            history_item = history_item_data.to_dict()
            history.append(history_item)

        best: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.best, Unset):
            best = self.best.to_dict()

        last: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.last, Unset):
            last = self.last.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "history": history,
            }
        )
        if best is not UNSET:
            field_dict["best"] = best
        if last is not UNSET:
            field_dict["last"] = last

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_metrics import ModelMetrics

        d = dict(src_dict)
        history = []
        _history = d.pop("history")
        for history_item_data in _history:
            history_item = ModelMetrics.from_dict(history_item_data)

            history.append(history_item)

        _best = d.pop("best", UNSET)
        best: Union[Unset, ModelMetrics]
        if isinstance(_best, Unset):
            best = UNSET
        else:
            best = ModelMetrics.from_dict(_best)

        _last = d.pop("last", UNSET)
        last: Union[Unset, ModelMetrics]
        if isinstance(_last, Unset):
            last = UNSET
        else:
            last = ModelMetrics.from_dict(_last)

        models_metrics = cls(
            history=history,
            best=best,
            last=last,
        )

        return models_metrics

from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GeneralToolbar")


@attr.s(auto_attribs=True)
class GeneralToolbar:
    """Second top bar general configuration

    Attributes:
        bar_color (Union[Unset, str]):
        text_color (Union[Unset, str]):
    """

    bar_color: Union[Unset, str] = UNSET
    text_color: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        bar_color = self.bar_color
        text_color = self.text_color

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if bar_color is not UNSET:
            field_dict["barColor"] = bar_color
        if text_color is not UNSET:
            field_dict["textColor"] = text_color

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bar_color = d.pop("barColor", UNSET)

        text_color = d.pop("textColor", UNSET)

        general_toolbar = cls(
            bar_color=bar_color,
            text_color=text_color,
        )

        return general_toolbar

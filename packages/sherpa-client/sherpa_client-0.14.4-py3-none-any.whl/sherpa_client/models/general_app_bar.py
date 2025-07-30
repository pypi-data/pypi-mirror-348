from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GeneralAppBar")


@attr.s(auto_attribs=True)
class GeneralAppBar:
    """Top bar general configuration

    Attributes:
        bar_color (Union[Unset, str]):
        icon_color (Union[Unset, str]):
        logo_is_grey (Union[Unset, bool]):  Default: True.
        logo_is_white (Union[Unset, bool]):
        text_color (Union[Unset, str]):
    """

    bar_color: Union[Unset, str] = UNSET
    icon_color: Union[Unset, str] = UNSET
    logo_is_grey: Union[Unset, bool] = True
    logo_is_white: Union[Unset, bool] = False
    text_color: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        bar_color = self.bar_color
        icon_color = self.icon_color
        logo_is_grey = self.logo_is_grey
        logo_is_white = self.logo_is_white
        text_color = self.text_color

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if bar_color is not UNSET:
            field_dict["barColor"] = bar_color
        if icon_color is not UNSET:
            field_dict["iconColor"] = icon_color
        if logo_is_grey is not UNSET:
            field_dict["logoIsGrey"] = logo_is_grey
        if logo_is_white is not UNSET:
            field_dict["logoIsWhite"] = logo_is_white
        if text_color is not UNSET:
            field_dict["textColor"] = text_color

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bar_color = d.pop("barColor", UNSET)

        icon_color = d.pop("iconColor", UNSET)

        logo_is_grey = d.pop("logoIsGrey", UNSET)

        logo_is_white = d.pop("logoIsWhite", UNSET)

        text_color = d.pop("textColor", UNSET)

        general_app_bar = cls(
            bar_color=bar_color,
            icon_color=icon_color,
            logo_is_grey=logo_is_grey,
            logo_is_white=logo_is_white,
            text_color=text_color,
        )

        return general_app_bar

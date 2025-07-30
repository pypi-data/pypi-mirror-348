from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GeneralFooter")


@attr.s(auto_attribs=True)
class GeneralFooter:
    """Bottom bar general configuration

    Attributes:
        footer_color (Union[Unset, str]):
        text_color (Union[Unset, str]):
    """

    footer_color: Union[Unset, str] = UNSET
    text_color: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        footer_color = self.footer_color
        text_color = self.text_color

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if footer_color is not UNSET:
            field_dict["footerColor"] = footer_color
        if text_color is not UNSET:
            field_dict["textColor"] = text_color

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        footer_color = d.pop("footerColor", UNSET)

        text_color = d.pop("textColor", UNSET)

        general_footer = cls(
            footer_color=footer_color,
            text_color=text_color,
        )

        return general_footer

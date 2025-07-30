from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="GeneralFooter")


@_attrs_define
class GeneralFooter:
    """Bottom bar general configuration

    Attributes:
        footer_color (Union[Unset, str]):
        text_color (Union[Unset, str]):
    """

    footer_color: Union[Unset, str] = UNSET
    text_color: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        footer_color = self.footer_color

        text_color = self.text_color

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if footer_color is not UNSET:
            field_dict["footerColor"] = footer_color
        if text_color is not UNSET:
            field_dict["textColor"] = text_color

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        footer_color = d.pop("footerColor", UNSET)

        text_color = d.pop("textColor", UNSET)

        general_footer = cls(
            footer_color=footer_color,
            text_color=text_color,
        )

        return general_footer

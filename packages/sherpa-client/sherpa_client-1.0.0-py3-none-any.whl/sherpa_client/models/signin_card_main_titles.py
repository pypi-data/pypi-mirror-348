from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SigninCardMainTitles")


@_attrs_define
class SigninCardMainTitles:
    """Main titles on signin page

    Attributes:
        en (Union[Unset, str]):  Default: 'Welcome to Kairntech'.
        fr (Union[Unset, str]):  Default: 'Bienvenue sur Kairntech'.
    """

    en: Union[Unset, str] = "Welcome to Kairntech"
    fr: Union[Unset, str] = "Bienvenue sur Kairntech"

    def to_dict(self) -> dict[str, Any]:
        en = self.en

        fr = self.fr

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if en is not UNSET:
            field_dict["en"] = en
        if fr is not UNSET:
            field_dict["fr"] = fr

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        en = d.pop("en", UNSET)

        fr = d.pop("fr", UNSET)

        signin_card_main_titles = cls(
            en=en,
            fr=fr,
        )

        return signin_card_main_titles

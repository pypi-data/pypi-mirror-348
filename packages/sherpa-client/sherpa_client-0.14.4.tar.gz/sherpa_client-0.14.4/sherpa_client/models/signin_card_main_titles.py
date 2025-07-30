from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SigninCardMainTitles")


@attr.s(auto_attribs=True)
class SigninCardMainTitles:
    """Main titles on signin page

    Attributes:
        en (Union[Unset, str]):  Default: 'Welcome to Kairntech'.
        fr (Union[Unset, str]):  Default: 'Bienvenue sur Kairntech'.
    """

    en: Union[Unset, str] = "Welcome to Kairntech"
    fr: Union[Unset, str] = "Bienvenue sur Kairntech"

    def to_dict(self) -> Dict[str, Any]:
        en = self.en
        fr = self.fr

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if en is not UNSET:
            field_dict["en"] = en
        if fr is not UNSET:
            field_dict["fr"] = fr

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        en = d.pop("en", UNSET)

        fr = d.pop("fr", UNSET)

        signin_card_main_titles = cls(
            en=en,
            fr=fr,
        )

        return signin_card_main_titles

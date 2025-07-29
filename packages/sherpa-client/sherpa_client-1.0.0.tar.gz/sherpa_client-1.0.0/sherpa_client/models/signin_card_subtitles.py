from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SigninCardSubtitles")


@_attrs_define
class SigninCardSubtitles:
    """Subtitles on signin page

    Attributes:
        en (Union[Unset, str]):  Default: 'AI language solutions for business users'.
        fr (Union[Unset, str]):  Default: "Solutions d'IA de traitement du langage".
    """

    en: Union[Unset, str] = "AI language solutions for business users"
    fr: Union[Unset, str] = "Solutions d'IA de traitement du langage"

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

        signin_card_subtitles = cls(
            en=en,
            fr=fr,
        )

        return signin_card_subtitles

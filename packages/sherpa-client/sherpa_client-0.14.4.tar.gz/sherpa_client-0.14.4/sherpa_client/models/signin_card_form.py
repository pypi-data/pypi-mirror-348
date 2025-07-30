from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.signin_card_main_titles import SigninCardMainTitles
    from ..models.signin_card_subtitles import SigninCardSubtitles


T = TypeVar("T", bound="SigninCardForm")


@attr.s(auto_attribs=True)
class SigninCardForm:
    """Form on signin page

    Attributes:
        btn_color (Union[Unset, str]):
        btn_text_color (Union[Unset, str]):
        card_bg_color (Union[Unset, str]):
        card_border_color (Union[Unset, str]):
        card_dark_mode (Union[Unset, bool]):
        card_opacity (Union[Unset, float]):  Default: 1.0.
        main_title (Union[Unset, SigninCardMainTitles]): Main titles on signin page
        subtitle (Union[Unset, SigninCardSubtitles]): Subtitles on signin page
        text_color (Union[Unset, str]):
    """

    btn_color: Union[Unset, str] = UNSET
    btn_text_color: Union[Unset, str] = UNSET
    card_bg_color: Union[Unset, str] = UNSET
    card_border_color: Union[Unset, str] = UNSET
    card_dark_mode: Union[Unset, bool] = False
    card_opacity: Union[Unset, float] = 1.0
    main_title: Union[Unset, "SigninCardMainTitles"] = UNSET
    subtitle: Union[Unset, "SigninCardSubtitles"] = UNSET
    text_color: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        btn_color = self.btn_color
        btn_text_color = self.btn_text_color
        card_bg_color = self.card_bg_color
        card_border_color = self.card_border_color
        card_dark_mode = self.card_dark_mode
        card_opacity = self.card_opacity
        main_title: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.main_title, Unset):
            main_title = self.main_title.to_dict()

        subtitle: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.subtitle, Unset):
            subtitle = self.subtitle.to_dict()

        text_color = self.text_color

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if btn_color is not UNSET:
            field_dict["btnColor"] = btn_color
        if btn_text_color is not UNSET:
            field_dict["btnTextColor"] = btn_text_color
        if card_bg_color is not UNSET:
            field_dict["cardBgColor"] = card_bg_color
        if card_border_color is not UNSET:
            field_dict["cardBorderColor"] = card_border_color
        if card_dark_mode is not UNSET:
            field_dict["cardDarkMode"] = card_dark_mode
        if card_opacity is not UNSET:
            field_dict["cardOpacity"] = card_opacity
        if main_title is not UNSET:
            field_dict["mainTitle"] = main_title
        if subtitle is not UNSET:
            field_dict["subtitle"] = subtitle
        if text_color is not UNSET:
            field_dict["textColor"] = text_color

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.signin_card_main_titles import SigninCardMainTitles
        from ..models.signin_card_subtitles import SigninCardSubtitles

        d = src_dict.copy()
        btn_color = d.pop("btnColor", UNSET)

        btn_text_color = d.pop("btnTextColor", UNSET)

        card_bg_color = d.pop("cardBgColor", UNSET)

        card_border_color = d.pop("cardBorderColor", UNSET)

        card_dark_mode = d.pop("cardDarkMode", UNSET)

        card_opacity = d.pop("cardOpacity", UNSET)

        _main_title = d.pop("mainTitle", UNSET)
        main_title: Union[Unset, SigninCardMainTitles]
        if isinstance(_main_title, Unset):
            main_title = UNSET
        else:
            main_title = SigninCardMainTitles.from_dict(_main_title)

        _subtitle = d.pop("subtitle", UNSET)
        subtitle: Union[Unset, SigninCardSubtitles]
        if isinstance(_subtitle, Unset):
            subtitle = UNSET
        else:
            subtitle = SigninCardSubtitles.from_dict(_subtitle)

        text_color = d.pop("textColor", UNSET)

        signin_card_form = cls(
            btn_color=btn_color,
            btn_text_color=btn_text_color,
            card_bg_color=card_bg_color,
            card_border_color=card_border_color,
            card_dark_mode=card_dark_mode,
            card_opacity=card_opacity,
            main_title=main_title,
            subtitle=subtitle,
            text_color=text_color,
        )

        return signin_card_form

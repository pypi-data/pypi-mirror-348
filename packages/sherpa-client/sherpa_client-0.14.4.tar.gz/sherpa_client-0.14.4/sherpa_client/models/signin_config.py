from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.signin_app_bar import SigninAppBar
    from ..models.signin_card_form import SigninCardForm
    from ..models.signin_footer import SigninFooter


T = TypeVar("T", bound="SigninConfig")


@attr.s(auto_attribs=True)
class SigninConfig:
    """Signin configuration

    Attributes:
        app_bar (Union[Unset, SigninAppBar]): Top bar on signin page
        card_form (Union[Unset, SigninCardForm]): Form on signin page
        footer (Union[Unset, SigninFooter]): Bottom bar on signin page
    """

    app_bar: Union[Unset, "SigninAppBar"] = UNSET
    card_form: Union[Unset, "SigninCardForm"] = UNSET
    footer: Union[Unset, "SigninFooter"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        app_bar: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.app_bar, Unset):
            app_bar = self.app_bar.to_dict()

        card_form: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.card_form, Unset):
            card_form = self.card_form.to_dict()

        footer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.footer, Unset):
            footer = self.footer.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if app_bar is not UNSET:
            field_dict["appBar"] = app_bar
        if card_form is not UNSET:
            field_dict["cardForm"] = card_form
        if footer is not UNSET:
            field_dict["footer"] = footer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.signin_app_bar import SigninAppBar
        from ..models.signin_card_form import SigninCardForm
        from ..models.signin_footer import SigninFooter

        d = src_dict.copy()
        _app_bar = d.pop("appBar", UNSET)
        app_bar: Union[Unset, SigninAppBar]
        if isinstance(_app_bar, Unset):
            app_bar = UNSET
        else:
            app_bar = SigninAppBar.from_dict(_app_bar)

        _card_form = d.pop("cardForm", UNSET)
        card_form: Union[Unset, SigninCardForm]
        if isinstance(_card_form, Unset):
            card_form = UNSET
        else:
            card_form = SigninCardForm.from_dict(_card_form)

        _footer = d.pop("footer", UNSET)
        footer: Union[Unset, SigninFooter]
        if isinstance(_footer, Unset):
            footer = UNSET
        else:
            footer = SigninFooter.from_dict(_footer)

        signin_config = cls(
            app_bar=app_bar,
            card_form=card_form,
            footer=footer,
        )

        return signin_config

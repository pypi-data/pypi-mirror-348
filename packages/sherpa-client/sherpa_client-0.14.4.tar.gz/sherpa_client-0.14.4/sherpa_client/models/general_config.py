from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.general_app_bar import GeneralAppBar
    from ..models.general_footer import GeneralFooter
    from ..models.general_toolbar import GeneralToolbar


T = TypeVar("T", bound="GeneralConfig")


@attr.s(auto_attribs=True)
class GeneralConfig:
    """General configuration

    Attributes:
        app_bar (Union[Unset, GeneralAppBar]): Top bar general configuration
        bar (Union[Unset, GeneralToolbar]): Second top bar general configuration
        footer (Union[Unset, GeneralFooter]): Bottom bar general configuration
    """

    app_bar: Union[Unset, "GeneralAppBar"] = UNSET
    bar: Union[Unset, "GeneralToolbar"] = UNSET
    footer: Union[Unset, "GeneralFooter"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        app_bar: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.app_bar, Unset):
            app_bar = self.app_bar.to_dict()

        bar: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bar, Unset):
            bar = self.bar.to_dict()

        footer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.footer, Unset):
            footer = self.footer.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if app_bar is not UNSET:
            field_dict["appBar"] = app_bar
        if bar is not UNSET:
            field_dict["bar"] = bar
        if footer is not UNSET:
            field_dict["footer"] = footer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.general_app_bar import GeneralAppBar
        from ..models.general_footer import GeneralFooter
        from ..models.general_toolbar import GeneralToolbar

        d = src_dict.copy()
        _app_bar = d.pop("appBar", UNSET)
        app_bar: Union[Unset, GeneralAppBar]
        if isinstance(_app_bar, Unset):
            app_bar = UNSET
        else:
            app_bar = GeneralAppBar.from_dict(_app_bar)

        _bar = d.pop("bar", UNSET)
        bar: Union[Unset, GeneralToolbar]
        if isinstance(_bar, Unset):
            bar = UNSET
        else:
            bar = GeneralToolbar.from_dict(_bar)

        _footer = d.pop("footer", UNSET)
        footer: Union[Unset, GeneralFooter]
        if isinstance(_footer, Unset):
            footer = UNSET
        else:
            footer = GeneralFooter.from_dict(_footer)

        general_config = cls(
            app_bar=app_bar,
            bar=bar,
            footer=footer,
        )

        return general_config

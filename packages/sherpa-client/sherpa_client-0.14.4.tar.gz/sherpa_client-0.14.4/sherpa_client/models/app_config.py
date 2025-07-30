from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.general_config import GeneralConfig
    from ..models.signin_config import SigninConfig
    from ..models.theme_media import ThemeMedia


T = TypeVar("T", bound="AppConfig")


@attr.s(auto_attribs=True)
class AppConfig:
    """
    Attributes:
        general (Union[Unset, GeneralConfig]): General configuration
        media (Union[Unset, ThemeMedia]): Images and videos on signin page
        signin (Union[Unset, SigninConfig]): Signin configuration
    """

    general: Union[Unset, "GeneralConfig"] = UNSET
    media: Union[Unset, "ThemeMedia"] = UNSET
    signin: Union[Unset, "SigninConfig"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        general: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.general, Unset):
            general = self.general.to_dict()

        media: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.media, Unset):
            media = self.media.to_dict()

        signin: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.signin, Unset):
            signin = self.signin.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if general is not UNSET:
            field_dict["general"] = general
        if media is not UNSET:
            field_dict["media"] = media
        if signin is not UNSET:
            field_dict["signin"] = signin

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.general_config import GeneralConfig
        from ..models.signin_config import SigninConfig
        from ..models.theme_media import ThemeMedia

        d = src_dict.copy()
        _general = d.pop("general", UNSET)
        general: Union[Unset, GeneralConfig]
        if isinstance(_general, Unset):
            general = UNSET
        else:
            general = GeneralConfig.from_dict(_general)

        _media = d.pop("media", UNSET)
        media: Union[Unset, ThemeMedia]
        if isinstance(_media, Unset):
            media = UNSET
        else:
            media = ThemeMedia.from_dict(_media)

        _signin = d.pop("signin", UNSET)
        signin: Union[Unset, SigninConfig]
        if isinstance(_signin, Unset):
            signin = UNSET
        else:
            signin = SigninConfig.from_dict(_signin)

        app_config = cls(
            general=general,
            media=media,
            signin=signin,
        )

        return app_config

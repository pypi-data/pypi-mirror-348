from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.share_mode import ShareMode


T = TypeVar("T", bound="PlatformShare")


@attr.s(auto_attribs=True)
class PlatformShare:
    """
    Attributes:
        can_revoke (bool):
        mode (ShareMode):
    """

    can_revoke: bool
    mode: "ShareMode"

    def to_dict(self) -> Dict[str, Any]:
        can_revoke = self.can_revoke
        mode = self.mode.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "canRevoke": can_revoke,
                "mode": mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.share_mode import ShareMode

        d = src_dict.copy()
        can_revoke = d.pop("canRevoke")

        mode = ShareMode.from_dict(d.pop("mode"))

        platform_share = cls(
            can_revoke=can_revoke,
            mode=mode,
        )

        return platform_share

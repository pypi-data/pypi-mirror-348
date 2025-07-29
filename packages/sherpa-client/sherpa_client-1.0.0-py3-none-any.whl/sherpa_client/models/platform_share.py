from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.share_mode import ShareMode


T = TypeVar("T", bound="PlatformShare")


@_attrs_define
class PlatformShare:
    """
    Attributes:
        can_revoke (bool):
        mode (ShareMode):
    """

    can_revoke: bool
    mode: "ShareMode"

    def to_dict(self) -> dict[str, Any]:
        can_revoke = self.can_revoke

        mode = self.mode.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "canRevoke": can_revoke,
                "mode": mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.share_mode import ShareMode

        d = dict(src_dict)
        can_revoke = d.pop("canRevoke")

        mode = ShareMode.from_dict(d.pop("mode"))

        platform_share = cls(
            can_revoke=can_revoke,
            mode=mode,
        )

        return platform_share

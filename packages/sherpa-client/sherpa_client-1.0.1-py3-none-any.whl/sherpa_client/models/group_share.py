from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.share_mode import ShareMode


T = TypeVar("T", bound="GroupShare")


@_attrs_define
class GroupShare:
    """
    Attributes:
        can_revoke (bool):
        group_name (str):
        mode (ShareMode):
    """

    can_revoke: bool
    group_name: str
    mode: "ShareMode"

    def to_dict(self) -> dict[str, Any]:
        can_revoke = self.can_revoke

        group_name = self.group_name

        mode = self.mode.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "canRevoke": can_revoke,
                "groupName": group_name,
                "mode": mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.share_mode import ShareMode

        d = dict(src_dict)
        can_revoke = d.pop("canRevoke")

        group_name = d.pop("groupName")

        mode = ShareMode.from_dict(d.pop("mode"))

        group_share = cls(
            can_revoke=can_revoke,
            group_name=group_name,
            mode=mode,
        )

        return group_share

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.share_mode import ShareMode


T = TypeVar("T", bound="UserShare")


@_attrs_define
class UserShare:
    """
    Attributes:
        mode (ShareMode):
        username (str):
    """

    mode: "ShareMode"
    username: str

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.to_dict()

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "mode": mode,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.share_mode import ShareMode

        d = dict(src_dict)
        mode = ShareMode.from_dict(d.pop("mode"))

        username = d.pop("username")

        user_share = cls(
            mode=mode,
            username=username,
        )

        return user_share

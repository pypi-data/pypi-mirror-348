from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.share_mode import ShareMode


T = TypeVar("T", bound="UserShare")


@attr.s(auto_attribs=True)
class UserShare:
    """
    Attributes:
        mode (ShareMode):
        username (str):
    """

    mode: "ShareMode"
    username: str

    def to_dict(self) -> Dict[str, Any]:
        mode = self.mode.to_dict()

        username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "mode": mode,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.share_mode import ShareMode

        d = src_dict.copy()
        mode = ShareMode.from_dict(d.pop("mode"))

        username = d.pop("username")

        user_share = cls(
            mode=mode,
            username=username,
        )

        return user_share

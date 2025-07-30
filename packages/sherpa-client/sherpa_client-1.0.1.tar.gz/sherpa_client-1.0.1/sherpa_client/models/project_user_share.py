from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.user_share import UserShare


T = TypeVar("T", bound="ProjectUserShare")


@_attrs_define
class ProjectUserShare:
    """
    Attributes:
        project_name (str):
        share (UserShare):
    """

    project_name: str
    share: "UserShare"

    def to_dict(self) -> dict[str, Any]:
        project_name = self.project_name

        share = self.share.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "projectName": project_name,
                "share": share,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_share import UserShare

        d = dict(src_dict)
        project_name = d.pop("projectName")

        share = UserShare.from_dict(d.pop("share"))

        project_user_share = cls(
            project_name=project_name,
            share=share,
        )

        return project_user_share

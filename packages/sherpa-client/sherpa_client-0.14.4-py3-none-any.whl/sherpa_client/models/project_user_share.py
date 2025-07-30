from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.user_share import UserShare


T = TypeVar("T", bound="ProjectUserShare")


@attr.s(auto_attribs=True)
class ProjectUserShare:
    """
    Attributes:
        project_name (str):
        share (UserShare):
    """

    project_name: str
    share: "UserShare"

    def to_dict(self) -> Dict[str, Any]:
        project_name = self.project_name
        share = self.share.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectName": project_name,
                "share": share,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_share import UserShare

        d = src_dict.copy()
        project_name = d.pop("projectName")

        share = UserShare.from_dict(d.pop("share"))

        project_user_share = cls(
            project_name=project_name,
            share=share,
        )

        return project_user_share

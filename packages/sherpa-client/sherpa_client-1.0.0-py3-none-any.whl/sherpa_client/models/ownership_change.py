from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.user_group_ref import UserGroupRef


T = TypeVar("T", bound="OwnershipChange")


@_attrs_define
class OwnershipChange:
    """
    Attributes:
        from_ (UserGroupRef):
        project_name (str):
        to (UserGroupRef):
    """

    from_: "UserGroupRef"
    project_name: str
    to: "UserGroupRef"

    def to_dict(self) -> dict[str, Any]:
        from_ = self.from_.to_dict()

        project_name = self.project_name

        to = self.to.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "from": from_,
                "projectName": project_name,
                "to": to,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_group_ref import UserGroupRef

        d = dict(src_dict)
        from_ = UserGroupRef.from_dict(d.pop("from"))

        project_name = d.pop("projectName")

        to = UserGroupRef.from_dict(d.pop("to"))

        ownership_change = cls(
            from_=from_,
            project_name=project_name,
            to=to,
        )

        return ownership_change

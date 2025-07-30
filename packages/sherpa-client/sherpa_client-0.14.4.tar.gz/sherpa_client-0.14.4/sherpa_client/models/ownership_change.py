from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.user_group_ref import UserGroupRef


T = TypeVar("T", bound="OwnershipChange")


@attr.s(auto_attribs=True)
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

    def to_dict(self) -> Dict[str, Any]:
        from_ = self.from_.to_dict()

        project_name = self.project_name
        to = self.to.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "from": from_,
                "projectName": project_name,
                "to": to,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_group_ref import UserGroupRef

        d = src_dict.copy()
        from_ = UserGroupRef.from_dict(d.pop("from"))

        project_name = d.pop("projectName")

        to = UserGroupRef.from_dict(d.pop("to"))

        ownership_change = cls(
            from_=from_,
            project_name=project_name,
            to=to,
        )

        return ownership_change

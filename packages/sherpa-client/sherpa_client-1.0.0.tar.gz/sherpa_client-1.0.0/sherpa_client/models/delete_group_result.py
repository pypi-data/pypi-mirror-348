from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DeleteGroupResult")


@_attrs_define
class DeleteGroupResult:
    """
    Attributes:
        removed_projects (int):
        removed_users (int):
    """

    removed_projects: int
    removed_users: int

    def to_dict(self) -> dict[str, Any]:
        removed_projects = self.removed_projects

        removed_users = self.removed_users

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "removedProjects": removed_projects,
                "removedUsers": removed_users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        removed_projects = d.pop("removedProjects")

        removed_users = d.pop("removedUsers")

        delete_group_result = cls(
            removed_projects=removed_projects,
            removed_users=removed_users,
        )

        return delete_group_result

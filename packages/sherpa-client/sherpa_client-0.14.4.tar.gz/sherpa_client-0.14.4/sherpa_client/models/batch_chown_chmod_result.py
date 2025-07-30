from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

import attr

if TYPE_CHECKING:
    from ..models.batch_errors import BatchErrors
    from ..models.ownership_change import OwnershipChange
    from ..models.project_user_share import ProjectUserShare


T = TypeVar("T", bound="BatchChownChmodResult")


@attr.s(auto_attribs=True)
class BatchChownChmodResult:
    """
    Attributes:
        errors (BatchErrors):
        non_chowned_projects (List[str]):
        ownership_changes (List['OwnershipChange']):
        project_user_shares (List['ProjectUserShare']):
    """

    errors: "BatchErrors"
    non_chowned_projects: List[str]
    ownership_changes: List["OwnershipChange"]
    project_user_shares: List["ProjectUserShare"]

    def to_dict(self) -> Dict[str, Any]:
        errors = self.errors.to_dict()

        non_chowned_projects = self.non_chowned_projects

        ownership_changes = []
        for ownership_changes_item_data in self.ownership_changes:
            ownership_changes_item = ownership_changes_item_data.to_dict()

            ownership_changes.append(ownership_changes_item)

        project_user_shares = []
        for project_user_shares_item_data in self.project_user_shares:
            project_user_shares_item = project_user_shares_item_data.to_dict()

            project_user_shares.append(project_user_shares_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "errors": errors,
                "nonChownedProjects": non_chowned_projects,
                "ownershipChanges": ownership_changes,
                "projectUserShares": project_user_shares,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.batch_errors import BatchErrors
        from ..models.ownership_change import OwnershipChange
        from ..models.project_user_share import ProjectUserShare

        d = src_dict.copy()
        errors = BatchErrors.from_dict(d.pop("errors"))

        non_chowned_projects = cast(List[str], d.pop("nonChownedProjects"))

        ownership_changes = []
        _ownership_changes = d.pop("ownershipChanges")
        for ownership_changes_item_data in _ownership_changes:
            ownership_changes_item = OwnershipChange.from_dict(ownership_changes_item_data)

            ownership_changes.append(ownership_changes_item)

        project_user_shares = []
        _project_user_shares = d.pop("projectUserShares")
        for project_user_shares_item_data in _project_user_shares:
            project_user_shares_item = ProjectUserShare.from_dict(project_user_shares_item_data)

            project_user_shares.append(project_user_shares_item)

        batch_chown_chmod_result = cls(
            errors=errors,
            non_chowned_projects=non_chowned_projects,
            ownership_changes=ownership_changes,
            project_user_shares=project_user_shares,
        )

        return batch_chown_chmod_result

from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="BatchErrors")


@attr.s(auto_attribs=True)
class BatchErrors:
    """
    Attributes:
        missing_project (List[str]):
        missing_project_group (List[str]):
        missing_project_owner (List[str]):
    """

    missing_project: List[str]
    missing_project_group: List[str]
    missing_project_owner: List[str]

    def to_dict(self) -> Dict[str, Any]:
        missing_project = self.missing_project

        missing_project_group = self.missing_project_group

        missing_project_owner = self.missing_project_owner

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "missingProject": missing_project,
                "missingProjectGroup": missing_project_group,
                "missingProjectOwner": missing_project_owner,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        missing_project = cast(List[str], d.pop("missingProject"))

        missing_project_group = cast(List[str], d.pop("missingProjectGroup"))

        missing_project_owner = cast(List[str], d.pop("missingProjectOwner"))

        batch_errors = cls(
            missing_project=missing_project,
            missing_project_group=missing_project_group,
            missing_project_owner=missing_project_owner,
        )

        return batch_errors

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="BatchErrors")


@_attrs_define
class BatchErrors:
    """
    Attributes:
        missing_project (list[str]):
        missing_project_group (list[str]):
        missing_project_owner (list[str]):
    """

    missing_project: list[str]
    missing_project_group: list[str]
    missing_project_owner: list[str]

    def to_dict(self) -> dict[str, Any]:
        missing_project = self.missing_project

        missing_project_group = self.missing_project_group

        missing_project_owner = self.missing_project_owner

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "missingProject": missing_project,
                "missingProjectGroup": missing_project_group,
                "missingProjectOwner": missing_project_owner,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        missing_project = cast(list[str], d.pop("missingProject"))

        missing_project_group = cast(list[str], d.pop("missingProjectGroup"))

        missing_project_owner = cast(list[str], d.pop("missingProjectOwner"))

        batch_errors = cls(
            missing_project=missing_project,
            missing_project_group=missing_project_group,
            missing_project_owner=missing_project_owner,
        )

        return batch_errors

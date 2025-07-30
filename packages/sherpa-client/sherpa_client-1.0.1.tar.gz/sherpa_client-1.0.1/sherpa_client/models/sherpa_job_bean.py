from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.sherpa_job_bean_status import SherpaJobBeanStatus
from ..models.sherpa_job_bean_type import SherpaJobBeanType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SherpaJobBean")


@_attrs_define
class SherpaJobBean:
    """
    Attributes:
        created_at (int):
        created_by (str):
        current_step_count (int):
        description (str):
        id (str):
        project (str):
        project_label (str):
        status (SherpaJobBeanStatus):
        total_step_count (int):
        type_ (SherpaJobBeanType):
        upload_ids (list[str]):
        completed_at (Union[Unset, int]):
        status_message (Union[Unset, str]):
    """

    created_at: int
    created_by: str
    current_step_count: int
    description: str
    id: str
    project: str
    project_label: str
    status: SherpaJobBeanStatus
    total_step_count: int
    type_: SherpaJobBeanType
    upload_ids: list[str]
    completed_at: Union[Unset, int] = UNSET
    status_message: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        created_by = self.created_by

        current_step_count = self.current_step_count

        description = self.description

        id = self.id

        project = self.project

        project_label = self.project_label

        status = self.status.value

        total_step_count = self.total_step_count

        type_ = self.type_.value

        upload_ids = self.upload_ids

        completed_at = self.completed_at

        status_message = self.status_message

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "createdAt": created_at,
                "createdBy": created_by,
                "currentStepCount": current_step_count,
                "description": description,
                "id": id,
                "project": project,
                "projectLabel": project_label,
                "status": status,
                "totalStepCount": total_step_count,
                "type": type_,
                "uploadIds": upload_ids,
            }
        )
        if completed_at is not UNSET:
            field_dict["completedAt"] = completed_at
        if status_message is not UNSET:
            field_dict["statusMessage"] = status_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = d.pop("createdAt")

        created_by = d.pop("createdBy")

        current_step_count = d.pop("currentStepCount")

        description = d.pop("description")

        id = d.pop("id")

        project = d.pop("project")

        project_label = d.pop("projectLabel")

        status = SherpaJobBeanStatus(d.pop("status"))

        total_step_count = d.pop("totalStepCount")

        type_ = SherpaJobBeanType(d.pop("type"))

        upload_ids = cast(list[str], d.pop("uploadIds"))

        completed_at = d.pop("completedAt", UNSET)

        status_message = d.pop("statusMessage", UNSET)

        sherpa_job_bean = cls(
            created_at=created_at,
            created_by=created_by,
            current_step_count=current_step_count,
            description=description,
            id=id,
            project=project,
            project_label=project_label,
            status=status,
            total_step_count=total_step_count,
            type_=type_,
            upload_ids=upload_ids,
            completed_at=completed_at,
            status_message=status_message,
        )

        return sherpa_job_bean

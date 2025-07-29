from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sherpa_job_bean import SherpaJobBean


T = TypeVar("T", bound="ProjectStatus")


@_attrs_define
class ProjectStatus:
    """
    Attributes:
        project_name (str):
        status (str):
        pending_job (Union[Unset, SherpaJobBean]):
    """

    project_name: str
    status: str
    pending_job: Union[Unset, "SherpaJobBean"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        project_name = self.project_name

        status = self.status

        pending_job: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.pending_job, Unset):
            pending_job = self.pending_job.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "projectName": project_name,
                "status": status,
            }
        )
        if pending_job is not UNSET:
            field_dict["pendingJob"] = pending_job

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sherpa_job_bean import SherpaJobBean

        d = dict(src_dict)
        project_name = d.pop("projectName")

        status = d.pop("status")

        _pending_job = d.pop("pendingJob", UNSET)
        pending_job: Union[Unset, SherpaJobBean]
        if isinstance(_pending_job, Unset):
            pending_job = UNSET
        else:
            pending_job = SherpaJobBean.from_dict(_pending_job)

        project_status = cls(
            project_name=project_name,
            status=status,
            pending_job=pending_job,
        )

        return project_status

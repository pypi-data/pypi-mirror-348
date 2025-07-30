from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.sherpa_job_bean import SherpaJobBean


T = TypeVar("T", bound="PlanOperationResponse")


@_attrs_define
class PlanOperationResponse:
    """
    Attributes:
        name (str):
        triggered_jobs (list['SherpaJobBean']):
    """

    name: str
    triggered_jobs: list["SherpaJobBean"]

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        triggered_jobs = []
        for triggered_jobs_item_data in self.triggered_jobs:
            triggered_jobs_item = triggered_jobs_item_data.to_dict()
            triggered_jobs.append(triggered_jobs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "triggeredJobs": triggered_jobs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sherpa_job_bean import SherpaJobBean

        d = dict(src_dict)
        name = d.pop("name")

        triggered_jobs = []
        _triggered_jobs = d.pop("triggeredJobs")
        for triggered_jobs_item_data in _triggered_jobs:
            triggered_jobs_item = SherpaJobBean.from_dict(triggered_jobs_item_data)

            triggered_jobs.append(triggered_jobs_item)

        plan_operation_response = cls(
            name=name,
            triggered_jobs=triggered_jobs,
        )

        return plan_operation_response

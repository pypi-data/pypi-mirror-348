from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.sherpa_job_bean import SherpaJobBean


T = TypeVar("T", bound="PlanOperationResponse")


@attr.s(auto_attribs=True)
class PlanOperationResponse:
    """
    Attributes:
        name (str):
        triggered_jobs (List['SherpaJobBean']):
    """

    name: str
    triggered_jobs: List["SherpaJobBean"]

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        triggered_jobs = []
        for triggered_jobs_item_data in self.triggered_jobs:
            triggered_jobs_item = triggered_jobs_item_data.to_dict()

            triggered_jobs.append(triggered_jobs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "triggeredJobs": triggered_jobs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sherpa_job_bean import SherpaJobBean

        d = src_dict.copy()
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

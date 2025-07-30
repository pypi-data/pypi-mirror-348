from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.item_count import ItemCount
    from ..models.sherpa_job_bean import SherpaJobBean


T = TypeVar("T", bound="DeleteManyResponse")


@attr.s(auto_attribs=True)
class DeleteManyResponse:
    """
    Attributes:
        removed (int):
        details (Union[Unset, List['ItemCount']]):
        job (Union[Unset, SherpaJobBean]):
    """

    removed: int
    details: Union[Unset, List["ItemCount"]] = UNSET
    job: Union[Unset, "SherpaJobBean"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        removed = self.removed
        details: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.details, Unset):
            details = []
            for details_item_data in self.details:
                details_item = details_item_data.to_dict()

                details.append(details_item)

        job: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.job, Unset):
            job = self.job.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "removed": removed,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details
        if job is not UNSET:
            field_dict["job"] = job

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.item_count import ItemCount
        from ..models.sherpa_job_bean import SherpaJobBean

        d = src_dict.copy()
        removed = d.pop("removed")

        details = []
        _details = d.pop("details", UNSET)
        for details_item_data in _details or []:
            details_item = ItemCount.from_dict(details_item_data)

            details.append(details_item)

        _job = d.pop("job", UNSET)
        job: Union[Unset, SherpaJobBean]
        if isinstance(_job, Unset):
            job = UNSET
        else:
            job = SherpaJobBean.from_dict(_job)

        delete_many_response = cls(
            removed=removed,
            details=details,
            job=job,
        )

        return delete_many_response

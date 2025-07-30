from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..models.project_open_session_state import ProjectOpenSessionState
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectOpenSession")


@_attrs_define
class ProjectOpenSession:
    """
    Attributes:
        campaign_id (str):
        duration (int):
        label (str):
        remaining_duration (int):
        session_id (str):
        state (ProjectOpenSessionState):
        id (Union[Unset, str]):
    """

    campaign_id: str
    duration: int
    label: str
    remaining_duration: int
    session_id: str
    state: ProjectOpenSessionState
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        campaign_id = self.campaign_id

        duration = self.duration

        label = self.label

        remaining_duration = self.remaining_duration

        session_id = self.session_id

        state = self.state.value

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "campaignId": campaign_id,
                "duration": duration,
                "label": label,
                "remainingDuration": remaining_duration,
                "sessionId": session_id,
                "state": state,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        campaign_id = d.pop("campaignId")

        duration = d.pop("duration")

        label = d.pop("label")

        remaining_duration = d.pop("remainingDuration")

        session_id = d.pop("sessionId")

        state = ProjectOpenSessionState(d.pop("state"))

        id = d.pop("id", UNSET)

        project_open_session = cls(
            campaign_id=campaign_id,
            duration=duration,
            label=label,
            remaining_duration=remaining_duration,
            session_id=session_id,
            state=state,
            id=id,
        )

        return project_open_session

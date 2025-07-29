from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_experiment_parameters import NewExperimentParameters


T = TypeVar("T", bound="NewExperiment")


@_attrs_define
class NewExperiment:
    """
    Attributes:
        engine (str):
        label (str):
        parameters (NewExperimentParameters):
        email_notification (Union[Unset, bool]):
        tags (Union[Unset, list[str]]):
    """

    engine: str
    label: str
    parameters: "NewExperimentParameters"
    email_notification: Union[Unset, bool] = UNSET
    tags: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        engine = self.engine

        label = self.label

        parameters = self.parameters.to_dict()

        email_notification = self.email_notification

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "engine": engine,
                "label": label,
                "parameters": parameters,
            }
        )
        if email_notification is not UNSET:
            field_dict["emailNotification"] = email_notification
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.new_experiment_parameters import NewExperimentParameters

        d = dict(src_dict)
        engine = d.pop("engine")

        label = d.pop("label")

        parameters = NewExperimentParameters.from_dict(d.pop("parameters"))

        email_notification = d.pop("emailNotification", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        new_experiment = cls(
            engine=engine,
            label=label,
            parameters=parameters,
            email_notification=email_notification,
            tags=tags,
        )

        return new_experiment

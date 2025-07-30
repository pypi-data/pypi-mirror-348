from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.gazetteer_parameters import GazetteerParameters


T = TypeVar("T", bound="Gazetteer")


@_attrs_define
class Gazetteer:
    """
    Attributes:
        duration (int):
        engine (str):
        label (str):
        models (int):
        name (str):
        parameters (GazetteerParameters):
        running (bool):
        timestamp (int):
        uptodate (bool):
        email_notification (Union[Unset, bool]):
        favorite (Union[Unset, bool]):
        tags (Union[Unset, list[str]]):
    """

    duration: int
    engine: str
    label: str
    models: int
    name: str
    parameters: "GazetteerParameters"
    running: bool
    timestamp: int
    uptodate: bool
    email_notification: Union[Unset, bool] = UNSET
    favorite: Union[Unset, bool] = UNSET
    tags: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        duration = self.duration

        engine = self.engine

        label = self.label

        models = self.models

        name = self.name

        parameters = self.parameters.to_dict()

        running = self.running

        timestamp = self.timestamp

        uptodate = self.uptodate

        email_notification = self.email_notification

        favorite = self.favorite

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "duration": duration,
                "engine": engine,
                "label": label,
                "models": models,
                "name": name,
                "parameters": parameters,
                "running": running,
                "timestamp": timestamp,
                "uptodate": uptodate,
            }
        )
        if email_notification is not UNSET:
            field_dict["emailNotification"] = email_notification
        if favorite is not UNSET:
            field_dict["favorite"] = favorite
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gazetteer_parameters import GazetteerParameters

        d = dict(src_dict)
        duration = d.pop("duration")

        engine = d.pop("engine")

        label = d.pop("label")

        models = d.pop("models")

        name = d.pop("name")

        parameters = GazetteerParameters.from_dict(d.pop("parameters"))

        running = d.pop("running")

        timestamp = d.pop("timestamp")

        uptodate = d.pop("uptodate")

        email_notification = d.pop("emailNotification", UNSET)

        favorite = d.pop("favorite", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        gazetteer = cls(
            duration=duration,
            engine=engine,
            label=label,
            models=models,
            name=name,
            parameters=parameters,
            running=running,
            timestamp=timestamp,
            uptodate=uptodate,
            email_notification=email_notification,
            favorite=favorite,
            tags=tags,
        )

        return gazetteer

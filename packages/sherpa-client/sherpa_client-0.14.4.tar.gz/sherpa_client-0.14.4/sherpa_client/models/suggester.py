from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.suggester_parameters import SuggesterParameters


T = TypeVar("T", bound="Suggester")


@attr.s(auto_attribs=True)
class Suggester:
    """
    Attributes:
        duration (int):
        engine (str):
        label (str):
        models (int):
        name (str):
        parameters (SuggesterParameters):
        quality (int):
        running (bool):
        timestamp (int):
        uptodate (bool):
        tags (Union[Unset, List[str]]):
    """

    duration: int
    engine: str
    label: str
    models: int
    name: str
    parameters: "SuggesterParameters"
    quality: int
    running: bool
    timestamp: int
    uptodate: bool
    tags: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        duration = self.duration
        engine = self.engine
        label = self.label
        models = self.models
        name = self.name
        parameters = self.parameters.to_dict()

        quality = self.quality
        running = self.running
        timestamp = self.timestamp
        uptodate = self.uptodate
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "duration": duration,
                "engine": engine,
                "label": label,
                "models": models,
                "name": name,
                "parameters": parameters,
                "quality": quality,
                "running": running,
                "timestamp": timestamp,
                "uptodate": uptodate,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.suggester_parameters import SuggesterParameters

        d = src_dict.copy()
        duration = d.pop("duration")

        engine = d.pop("engine")

        label = d.pop("label")

        models = d.pop("models")

        name = d.pop("name")

        parameters = SuggesterParameters.from_dict(d.pop("parameters"))

        quality = d.pop("quality")

        running = d.pop("running")

        timestamp = d.pop("timestamp")

        uptodate = d.pop("uptodate")

        tags = cast(List[str], d.pop("tags", UNSET))

        suggester = cls(
            duration=duration,
            engine=engine,
            label=label,
            models=models,
            name=name,
            parameters=parameters,
            quality=quality,
            running=running,
            timestamp=timestamp,
            uptodate=uptodate,
            tags=tags,
        )

        return suggester

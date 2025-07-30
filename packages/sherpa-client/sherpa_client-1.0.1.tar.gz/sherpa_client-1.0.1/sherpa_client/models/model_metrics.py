from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.engine_config import EngineConfig
    from ..models.model_metrics_options import ModelMetricsOptions
    from ..models.report import Report


T = TypeVar("T", bound="ModelMetrics")


@_attrs_define
class ModelMetrics:
    """
    Attributes:
        classes (list[str]):
        config (EngineConfig):
        engine (str):
        lang (str):
        name (str):
        options (ModelMetricsOptions):
        quality (float):
        report (Report):
        status (str):
        timestamp (int):
        timestamp_end (int):
    """

    classes: list[str]
    config: "EngineConfig"
    engine: str
    lang: str
    name: str
    options: "ModelMetricsOptions"
    quality: float
    report: "Report"
    status: str
    timestamp: int
    timestamp_end: int

    def to_dict(self) -> dict[str, Any]:
        classes = self.classes

        config = self.config.to_dict()

        engine = self.engine

        lang = self.lang

        name = self.name

        options = self.options.to_dict()

        quality = self.quality

        report = self.report.to_dict()

        status = self.status

        timestamp = self.timestamp

        timestamp_end = self.timestamp_end

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "classes": classes,
                "config": config,
                "engine": engine,
                "lang": lang,
                "name": name,
                "options": options,
                "quality": quality,
                "report": report,
                "status": status,
                "timestamp": timestamp,
                "timestamp_end": timestamp_end,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.engine_config import EngineConfig
        from ..models.model_metrics_options import ModelMetricsOptions
        from ..models.report import Report

        d = dict(src_dict)
        classes = cast(list[str], d.pop("classes"))

        config = EngineConfig.from_dict(d.pop("config"))

        engine = d.pop("engine")

        lang = d.pop("lang")

        name = d.pop("name")

        options = ModelMetricsOptions.from_dict(d.pop("options"))

        quality = d.pop("quality")

        report = Report.from_dict(d.pop("report"))

        status = d.pop("status")

        timestamp = d.pop("timestamp")

        timestamp_end = d.pop("timestamp_end")

        model_metrics = cls(
            classes=classes,
            config=config,
            engine=engine,
            lang=lang,
            name=name,
            options=options,
            quality=quality,
            report=report,
            status=status,
            timestamp=timestamp,
            timestamp_end=timestamp_end,
        )

        return model_metrics

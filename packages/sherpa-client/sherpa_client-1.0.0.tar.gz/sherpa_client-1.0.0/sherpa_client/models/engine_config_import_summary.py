from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sherpa_job_bean import SherpaJobBean


T = TypeVar("T", bound="EngineConfigImportSummary")


@_attrs_define
class EngineConfigImportSummary:
    """
    Attributes:
        configs (Union[Unset, list[str]]):
        ignored (Union[Unset, list[str]]):
        models (Union[Unset, int]): number of models that will be imported Default: 0.
        pending_job (Union[Unset, SherpaJobBean]):
    """

    configs: Union[Unset, list[str]] = UNSET
    ignored: Union[Unset, list[str]] = UNSET
    models: Union[Unset, int] = 0
    pending_job: Union[Unset, "SherpaJobBean"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        configs: Union[Unset, list[str]] = UNSET
        if not isinstance(self.configs, Unset):
            configs = self.configs

        ignored: Union[Unset, list[str]] = UNSET
        if not isinstance(self.ignored, Unset):
            ignored = self.ignored

        models = self.models

        pending_job: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.pending_job, Unset):
            pending_job = self.pending_job.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if configs is not UNSET:
            field_dict["configs"] = configs
        if ignored is not UNSET:
            field_dict["ignored"] = ignored
        if models is not UNSET:
            field_dict["models"] = models
        if pending_job is not UNSET:
            field_dict["pendingJob"] = pending_job

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sherpa_job_bean import SherpaJobBean

        d = dict(src_dict)
        configs = cast(list[str], d.pop("configs", UNSET))

        ignored = cast(list[str], d.pop("ignored", UNSET))

        models = d.pop("models", UNSET)

        _pending_job = d.pop("pendingJob", UNSET)
        pending_job: Union[Unset, SherpaJobBean]
        if isinstance(_pending_job, Unset):
            pending_job = UNSET
        else:
            pending_job = SherpaJobBean.from_dict(_pending_job)

        engine_config_import_summary = cls(
            configs=configs,
            ignored=ignored,
            models=models,
            pending_job=pending_job,
        )

        return engine_config_import_summary

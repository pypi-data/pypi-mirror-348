from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.apply_to import ApplyTo
    from ..models.with_vectorizer_condition import WithVectorizerCondition
    from ..models.with_vectorizer_parameters import WithVectorizerParameters


T = TypeVar("T", bound="WithVectorizer")


@_attrs_define
class WithVectorizer:
    """
    Attributes:
        vectorizer (str):
        apply_to (Union[Unset, ApplyTo]):
        condition (Union[Unset, WithVectorizerCondition]):
        disabled (Union[Unset, bool]):
        parameters (Union[Unset, WithVectorizerParameters]):
        project_name (Union[Unset, str]):
    """

    vectorizer: str
    apply_to: Union[Unset, "ApplyTo"] = UNSET
    condition: Union[Unset, "WithVectorizerCondition"] = UNSET
    disabled: Union[Unset, bool] = UNSET
    parameters: Union[Unset, "WithVectorizerParameters"] = UNSET
    project_name: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        vectorizer = self.vectorizer

        apply_to: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.apply_to, Unset):
            apply_to = self.apply_to.to_dict()

        condition: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.condition, Unset):
            condition = self.condition.to_dict()

        disabled = self.disabled

        parameters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        project_name = self.project_name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "vectorizer": vectorizer,
            }
        )
        if apply_to is not UNSET:
            field_dict["applyTo"] = apply_to
        if condition is not UNSET:
            field_dict["condition"] = condition
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if project_name is not UNSET:
            field_dict["projectName"] = project_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.apply_to import ApplyTo
        from ..models.with_vectorizer_condition import WithVectorizerCondition
        from ..models.with_vectorizer_parameters import WithVectorizerParameters

        d = dict(src_dict)
        vectorizer = d.pop("vectorizer")

        _apply_to = d.pop("applyTo", UNSET)
        apply_to: Union[Unset, ApplyTo]
        if isinstance(_apply_to, Unset):
            apply_to = UNSET
        else:
            apply_to = ApplyTo.from_dict(_apply_to)

        _condition = d.pop("condition", UNSET)
        condition: Union[Unset, WithVectorizerCondition]
        if isinstance(_condition, Unset):
            condition = UNSET
        else:
            condition = WithVectorizerCondition.from_dict(_condition)

        disabled = d.pop("disabled", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, WithVectorizerParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = WithVectorizerParameters.from_dict(_parameters)

        project_name = d.pop("projectName", UNSET)

        with_vectorizer = cls(
            vectorizer=vectorizer,
            apply_to=apply_to,
            condition=condition,
            disabled=disabled,
            parameters=parameters,
            project_name=project_name,
        )

        return with_vectorizer

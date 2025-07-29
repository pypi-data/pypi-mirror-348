from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..models.question_answering_params_language_detection import (
    QuestionAnsweringParamsLanguageDetection,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="QuestionAnsweringParams")


@_attrs_define
class QuestionAnsweringParams:
    """Question answering parameters

    Attributes:
        answer_language (Union[Unset, str]): Language of the answer (overrides languageSource)
        enabled (Union[Unset, bool]): Generate answer to the question Default: False.
        generator (Union[Unset, str]): Answer generator to be used
        language_detection (Union[Unset, QuestionAnsweringParamsLanguageDetection]): Source used to decide the language
            of the answer Default: QuestionAnsweringParamsLanguageDetection.PROJECT.
        query (Union[Unset, str]):
    """

    answer_language: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = False
    generator: Union[Unset, str] = UNSET
    language_detection: Union[Unset, QuestionAnsweringParamsLanguageDetection] = (
        QuestionAnsweringParamsLanguageDetection.PROJECT
    )
    query: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        answer_language = self.answer_language

        enabled = self.enabled

        generator = self.generator

        language_detection: Union[Unset, str] = UNSET
        if not isinstance(self.language_detection, Unset):
            language_detection = self.language_detection.value

        query = self.query

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if answer_language is not UNSET:
            field_dict["answerLanguage"] = answer_language
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if generator is not UNSET:
            field_dict["generator"] = generator
        if language_detection is not UNSET:
            field_dict["languageDetection"] = language_detection
        if query is not UNSET:
            field_dict["query"] = query

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        answer_language = d.pop("answerLanguage", UNSET)

        enabled = d.pop("enabled", UNSET)

        generator = d.pop("generator", UNSET)

        _language_detection = d.pop("languageDetection", UNSET)
        language_detection: Union[Unset, QuestionAnsweringParamsLanguageDetection]
        if isinstance(_language_detection, Unset):
            language_detection = UNSET
        else:
            language_detection = QuestionAnsweringParamsLanguageDetection(
                _language_detection
            )

        query = d.pop("query", UNSET)

        question_answering_params = cls(
            answer_language=answer_language,
            enabled=enabled,
            generator=generator,
            language_detection=language_detection,
            query=query,
        )

        return question_answering_params

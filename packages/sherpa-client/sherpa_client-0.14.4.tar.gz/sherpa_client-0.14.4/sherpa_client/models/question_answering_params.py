from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.question_answering_params_language_detection import QuestionAnsweringParamsLanguageDetection
from ..types import UNSET, Unset

T = TypeVar("T", bound="QuestionAnsweringParams")


@attr.s(auto_attribs=True)
class QuestionAnsweringParams:
    """Question answering parameters

    Attributes:
        answer_language (Union[Unset, str]): Language of the answer (overrides languageSource)
        context (Union[Unset, bool]): Generate answer to the question
        context_only (Union[Unset, bool]):
        enabled (Union[Unset, bool]): Generate answer to the question
        generator (Union[Unset, str]): Answer generator to be used
        html (Union[Unset, bool]):
        language_detection (Union[Unset, QuestionAnsweringParamsLanguageDetection]): Source used to decide the language
            of the answer Default: QuestionAnsweringParamsLanguageDetection.PROJECT.
        query (Union[Unset, str]):
    """

    answer_language: Union[Unset, str] = UNSET
    context: Union[Unset, bool] = False
    context_only: Union[Unset, bool] = False
    enabled: Union[Unset, bool] = False
    generator: Union[Unset, str] = UNSET
    html: Union[Unset, bool] = False
    language_detection: Union[
        Unset, QuestionAnsweringParamsLanguageDetection
    ] = QuestionAnsweringParamsLanguageDetection.PROJECT
    query: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        answer_language = self.answer_language
        context = self.context
        context_only = self.context_only
        enabled = self.enabled
        generator = self.generator
        html = self.html
        language_detection: Union[Unset, str] = UNSET
        if not isinstance(self.language_detection, Unset):
            language_detection = self.language_detection.value

        query = self.query

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if answer_language is not UNSET:
            field_dict["answerLanguage"] = answer_language
        if context is not UNSET:
            field_dict["context"] = context
        if context_only is not UNSET:
            field_dict["contextOnly"] = context_only
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if generator is not UNSET:
            field_dict["generator"] = generator
        if html is not UNSET:
            field_dict["html"] = html
        if language_detection is not UNSET:
            field_dict["languageDetection"] = language_detection
        if query is not UNSET:
            field_dict["query"] = query

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        answer_language = d.pop("answerLanguage", UNSET)

        context = d.pop("context", UNSET)

        context_only = d.pop("contextOnly", UNSET)

        enabled = d.pop("enabled", UNSET)

        generator = d.pop("generator", UNSET)

        html = d.pop("html", UNSET)

        _language_detection = d.pop("languageDetection", UNSET)
        language_detection: Union[Unset, QuestionAnsweringParamsLanguageDetection]
        if isinstance(_language_detection, Unset):
            language_detection = UNSET
        else:
            language_detection = QuestionAnsweringParamsLanguageDetection(_language_detection)

        query = d.pop("query", UNSET)

        question_answering_params = cls(
            answer_language=answer_language,
            context=context,
            context_only=context_only,
            enabled=enabled,
            generator=generator,
            html=html,
            language_detection=language_detection,
            query=query,
        )

        return question_answering_params

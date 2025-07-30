from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.output_params import OutputParams
    from ..models.question_answering_params import QuestionAnsweringParams
    from ..models.search_params import SearchParams


T = TypeVar("T", bound="SearchRequest")


@attr.s(auto_attribs=True)
class SearchRequest:
    """Search request

    Attributes:
        output (Union[Unset, OutputParams]): Search output parameters
        question_answering (Union[Unset, QuestionAnsweringParams]): Question answering parameters
        search (Union[Unset, SearchParams]): Search parameters
    """

    output: Union[Unset, "OutputParams"] = UNSET
    question_answering: Union[Unset, "QuestionAnsweringParams"] = UNSET
    search: Union[Unset, "SearchParams"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        output: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.output, Unset):
            output = self.output.to_dict()

        question_answering: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.question_answering, Unset):
            question_answering = self.question_answering.to_dict()

        search: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.search, Unset):
            search = self.search.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if output is not UNSET:
            field_dict["output"] = output
        if question_answering is not UNSET:
            field_dict["questionAnswering"] = question_answering
        if search is not UNSET:
            field_dict["search"] = search

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.output_params import OutputParams
        from ..models.question_answering_params import QuestionAnsweringParams
        from ..models.search_params import SearchParams

        d = src_dict.copy()
        _output = d.pop("output", UNSET)
        output: Union[Unset, OutputParams]
        if isinstance(_output, Unset):
            output = UNSET
        else:
            output = OutputParams.from_dict(_output)

        _question_answering = d.pop("questionAnswering", UNSET)
        question_answering: Union[Unset, QuestionAnsweringParams]
        if isinstance(_question_answering, Unset):
            question_answering = UNSET
        else:
            question_answering = QuestionAnsweringParams.from_dict(_question_answering)

        _search = d.pop("search", UNSET)
        search: Union[Unset, SearchParams]
        if isinstance(_search, Unset):
            search = UNSET
        else:
            search = SearchParams.from_dict(_search)

        search_request = cls(
            output=output,
            question_answering=question_answering,
            search=search,
        )

        return search_request

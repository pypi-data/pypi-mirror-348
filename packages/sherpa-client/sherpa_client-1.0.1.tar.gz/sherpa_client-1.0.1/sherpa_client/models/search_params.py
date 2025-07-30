from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..models.search_params_type import SearchParamsType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filtering_params import FilteringParams
    from ..models.vector_params import VectorParams


T = TypeVar("T", bound="SearchParams")


@_attrs_define
class SearchParams:
    """Search parameters

    Attributes:
        advanced (Union[Unset, bool]): Full lucene syntax will be used, but syntax errors may occur (for advanced users
            only) Default: False.
        filtering (Union[Unset, FilteringParams]): Filtering parameters
        from_ (Union[Unset, int]): Offset of the first hit to be returned Default: 0.
        invert (Union[Unset, bool]): Return hits not matching the query Default: False.
        query (Union[Unset, str]): Search keywords or question
        size (Union[Unset, int]): Maximum number of hits to be returned Default: 10.
        type_ (Union[Unset, SearchParamsType]): Whether to use standard text-based, vector-based or hybrid search
            Default: SearchParamsType.TEXT.
        vector (Union[Unset, VectorParams]): Vector or hybrid search parameters
    """

    advanced: Union[Unset, bool] = False
    filtering: Union[Unset, "FilteringParams"] = UNSET
    from_: Union[Unset, int] = 0
    invert: Union[Unset, bool] = False
    query: Union[Unset, str] = UNSET
    size: Union[Unset, int] = 10
    type_: Union[Unset, SearchParamsType] = SearchParamsType.TEXT
    vector: Union[Unset, "VectorParams"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        advanced = self.advanced

        filtering: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filtering, Unset):
            filtering = self.filtering.to_dict()

        from_ = self.from_

        invert = self.invert

        query = self.query

        size = self.size

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        vector: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.vector, Unset):
            vector = self.vector.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if advanced is not UNSET:
            field_dict["advanced"] = advanced
        if filtering is not UNSET:
            field_dict["filtering"] = filtering
        if from_ is not UNSET:
            field_dict["from"] = from_
        if invert is not UNSET:
            field_dict["invert"] = invert
        if query is not UNSET:
            field_dict["query"] = query
        if size is not UNSET:
            field_dict["size"] = size
        if type_ is not UNSET:
            field_dict["type"] = type_
        if vector is not UNSET:
            field_dict["vector"] = vector

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filtering_params import FilteringParams
        from ..models.vector_params import VectorParams

        d = dict(src_dict)
        advanced = d.pop("advanced", UNSET)

        _filtering = d.pop("filtering", UNSET)
        filtering: Union[Unset, FilteringParams]
        if isinstance(_filtering, Unset):
            filtering = UNSET
        else:
            filtering = FilteringParams.from_dict(_filtering)

        from_ = d.pop("from", UNSET)

        invert = d.pop("invert", UNSET)

        query = d.pop("query", UNSET)

        size = d.pop("size", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, SearchParamsType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = SearchParamsType(_type_)

        _vector = d.pop("vector", UNSET)
        vector: Union[Unset, VectorParams]
        if isinstance(_vector, Unset):
            vector = UNSET
        else:
            vector = VectorParams.from_dict(_vector)

        search_params = cls(
            advanced=advanced,
            filtering=filtering,
            from_=from_,
            invert=invert,
            query=query,
            size=size,
            type_=type_,
            vector=vector,
        )

        return search_params

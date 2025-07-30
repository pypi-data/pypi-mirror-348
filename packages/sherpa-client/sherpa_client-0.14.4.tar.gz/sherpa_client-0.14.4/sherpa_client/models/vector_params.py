from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.vector_params_native_rrf import VectorParamsNativeRRF
from ..types import UNSET, Unset

T = TypeVar("T", bound="VectorParams")


@attr.s(auto_attribs=True)
class VectorParams:
    """Vector or hybrid search parameters

    Attributes:
        native_rrf (Union[Unset, VectorParamsNativeRRF]): Use native RRF implementation (for hybrid search) Default:
            VectorParamsNativeRRF.IF_AVAILABLE.
        query (Union[Unset, str]): Sentence or question to be vectorized (if it must be different from the general
            query; if not defined, the general query is used)
        vectorizer (Union[Unset, str]): Vectorizer to be used in case of vector-based or hybrid search (name of a
            vectorization pipeline)
    """

    native_rrf: Union[Unset, VectorParamsNativeRRF] = VectorParamsNativeRRF.IF_AVAILABLE
    query: Union[Unset, str] = UNSET
    vectorizer: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        native_rrf: Union[Unset, str] = UNSET
        if not isinstance(self.native_rrf, Unset):
            native_rrf = self.native_rrf.value

        query = self.query
        vectorizer = self.vectorizer

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if native_rrf is not UNSET:
            field_dict["nativeRRF"] = native_rrf
        if query is not UNSET:
            field_dict["query"] = query
        if vectorizer is not UNSET:
            field_dict["vectorizer"] = vectorizer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _native_rrf = d.pop("nativeRRF", UNSET)
        native_rrf: Union[Unset, VectorParamsNativeRRF]
        if isinstance(_native_rrf, Unset):
            native_rrf = UNSET
        else:
            native_rrf = VectorParamsNativeRRF(_native_rrf)

        query = d.pop("query", UNSET)

        vectorizer = d.pop("vectorizer", UNSET)

        vector_params = cls(
            native_rrf=native_rrf,
            query=query,
            vectorizer=vectorizer,
        )

        return vector_params

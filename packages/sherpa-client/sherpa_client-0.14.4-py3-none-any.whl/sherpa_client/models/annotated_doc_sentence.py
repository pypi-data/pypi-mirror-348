from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotated_doc_category import AnnotatedDocCategory
    from ..models.annotated_doc_sentence_metadata import AnnotatedDocSentenceMetadata


T = TypeVar("T", bound="AnnotatedDocSentence")


@attr.s(auto_attribs=True)
class AnnotatedDocSentence:
    """
    Attributes:
        end (int):
        start (int):
        categories (Union[Unset, List['AnnotatedDocCategory']]):
        metadata (Union[Unset, AnnotatedDocSentenceMetadata]):
        text (Union[Unset, str]):
    """

    end: int
    start: int
    categories: Union[Unset, List["AnnotatedDocCategory"]] = UNSET
    metadata: Union[Unset, "AnnotatedDocSentenceMetadata"] = UNSET
    text: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        end = self.end
        start = self.start
        categories: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()

                categories.append(categories_item)

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "end": end,
                "start": start,
            }
        )
        if categories is not UNSET:
            field_dict["categories"] = categories
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.annotated_doc_category import AnnotatedDocCategory
        from ..models.annotated_doc_sentence_metadata import AnnotatedDocSentenceMetadata

        d = src_dict.copy()
        end = d.pop("end")

        start = d.pop("start")

        categories = []
        _categories = d.pop("categories", UNSET)
        for categories_item_data in _categories or []:
            categories_item = AnnotatedDocCategory.from_dict(categories_item_data)

            categories.append(categories_item)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, AnnotatedDocSentenceMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = AnnotatedDocSentenceMetadata.from_dict(_metadata)

        text = d.pop("text", UNSET)

        annotated_doc_sentence = cls(
            end=end,
            start=start,
            categories=categories,
            metadata=metadata,
            text=text,
        )

        return annotated_doc_sentence

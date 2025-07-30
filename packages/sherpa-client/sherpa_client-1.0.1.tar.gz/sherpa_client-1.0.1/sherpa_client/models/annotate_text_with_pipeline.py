from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.with_annotator import WithAnnotator
    from ..models.with_converter import WithConverter
    from ..models.with_language_guesser import WithLanguageGuesser
    from ..models.with_processor import WithProcessor
    from ..models.with_segmenter import WithSegmenter
    from ..models.with_vectorizer import WithVectorizer


T = TypeVar("T", bound="AnnotateTextWithPipeline")


@_attrs_define
class AnnotateTextWithPipeline:
    """
    Attributes:
        pipeline (list[Union['WithAnnotator', 'WithConverter', 'WithLanguageGuesser', 'WithProcessor', 'WithSegmenter',
            'WithVectorizer']]):
        text (str): Text to be annotated
    """

    pipeline: list[
        Union[
            "WithAnnotator",
            "WithConverter",
            "WithLanguageGuesser",
            "WithProcessor",
            "WithSegmenter",
            "WithVectorizer",
        ]
    ]
    text: str

    def to_dict(self) -> dict[str, Any]:
        from ..models.with_annotator import WithAnnotator
        from ..models.with_converter import WithConverter
        from ..models.with_language_guesser import WithLanguageGuesser
        from ..models.with_processor import WithProcessor
        from ..models.with_segmenter import WithSegmenter

        pipeline = []
        for pipeline_item_data in self.pipeline:
            pipeline_item: dict[str, Any]
            if isinstance(pipeline_item_data, WithAnnotator):
                pipeline_item = pipeline_item_data.to_dict()
            elif isinstance(pipeline_item_data, WithProcessor):
                pipeline_item = pipeline_item_data.to_dict()
            elif isinstance(pipeline_item_data, WithLanguageGuesser):
                pipeline_item = pipeline_item_data.to_dict()
            elif isinstance(pipeline_item_data, WithSegmenter):
                pipeline_item = pipeline_item_data.to_dict()
            elif isinstance(pipeline_item_data, WithConverter):
                pipeline_item = pipeline_item_data.to_dict()
            else:
                pipeline_item = pipeline_item_data.to_dict()

            pipeline.append(pipeline_item)

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "pipeline": pipeline,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.with_annotator import WithAnnotator
        from ..models.with_converter import WithConverter
        from ..models.with_language_guesser import WithLanguageGuesser
        from ..models.with_processor import WithProcessor
        from ..models.with_segmenter import WithSegmenter
        from ..models.with_vectorizer import WithVectorizer

        d = dict(src_dict)
        pipeline = []
        _pipeline = d.pop("pipeline")
        for pipeline_item_data in _pipeline:

            def _parse_pipeline_item(
                data: object,
            ) -> Union[
                "WithAnnotator",
                "WithConverter",
                "WithLanguageGuesser",
                "WithProcessor",
                "WithSegmenter",
                "WithVectorizer",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    pipeline_item_type_0 = WithAnnotator.from_dict(data)

                    return pipeline_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    pipeline_item_type_1 = WithProcessor.from_dict(data)

                    return pipeline_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    pipeline_item_type_2 = WithLanguageGuesser.from_dict(data)

                    return pipeline_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    pipeline_item_type_3 = WithSegmenter.from_dict(data)

                    return pipeline_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    pipeline_item_type_4 = WithConverter.from_dict(data)

                    return pipeline_item_type_4
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                pipeline_item_type_5 = WithVectorizer.from_dict(data)

                return pipeline_item_type_5

            pipeline_item = _parse_pipeline_item(pipeline_item_data)

            pipeline.append(pipeline_item)

        text = d.pop("text")

        annotate_text_with_pipeline = cls(
            pipeline=pipeline,
            text=text,
        )

        return annotate_text_with_pipeline

from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.http_service_metadata_operations import HttpServiceMetadataOperations
    from ..models.http_service_metadata_service import HttpServiceMetadataService


T = TypeVar("T", bound="HttpServiceMetadata")


@attr.s(auto_attribs=True)
class HttpServiceMetadata:
    """
    Attributes:
        api (str):
        compatibility (str):
        version (str):
        annotators (Union[Unset, str]):
        converters (Union[Unset, str]):
        engine (Union[Unset, str]):
        extensions (Union[Unset, str]):
        formatters (Union[Unset, str]):
        functions (Union[Unset, str]):
        keep_alive (Union[Unset, bool]):
        language_guessers (Union[Unset, str]):
        languages (Union[Unset, str]):
        name (Union[Unset, str]):
        natures (Union[Unset, str]):
        operations (Union[Unset, HttpServiceMetadataOperations]):
        processors (Union[Unset, str]):
        segmenters (Union[Unset, str]):
        service (Union[Unset, HttpServiceMetadataService]):
        term_importers (Union[Unset, str]):
        trigger (Union[Unset, str]):
        vectorizers (Union[Unset, str]):
    """

    api: str
    compatibility: str
    version: str
    annotators: Union[Unset, str] = UNSET
    converters: Union[Unset, str] = UNSET
    engine: Union[Unset, str] = UNSET
    extensions: Union[Unset, str] = UNSET
    formatters: Union[Unset, str] = UNSET
    functions: Union[Unset, str] = UNSET
    keep_alive: Union[Unset, bool] = UNSET
    language_guessers: Union[Unset, str] = UNSET
    languages: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    natures: Union[Unset, str] = UNSET
    operations: Union[Unset, "HttpServiceMetadataOperations"] = UNSET
    processors: Union[Unset, str] = UNSET
    segmenters: Union[Unset, str] = UNSET
    service: Union[Unset, "HttpServiceMetadataService"] = UNSET
    term_importers: Union[Unset, str] = UNSET
    trigger: Union[Unset, str] = UNSET
    vectorizers: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        api = self.api
        compatibility = self.compatibility
        version = self.version
        annotators = self.annotators
        converters = self.converters
        engine = self.engine
        extensions = self.extensions
        formatters = self.formatters
        functions = self.functions
        keep_alive = self.keep_alive
        language_guessers = self.language_guessers
        languages = self.languages
        name = self.name
        natures = self.natures
        operations: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.operations, Unset):
            operations = self.operations.to_dict()

        processors = self.processors
        segmenters = self.segmenters
        service: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.service, Unset):
            service = self.service.to_dict()

        term_importers = self.term_importers
        trigger = self.trigger
        vectorizers = self.vectorizers

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "api": api,
                "compatibility": compatibility,
                "version": version,
            }
        )
        if annotators is not UNSET:
            field_dict["annotators"] = annotators
        if converters is not UNSET:
            field_dict["converters"] = converters
        if engine is not UNSET:
            field_dict["engine"] = engine
        if extensions is not UNSET:
            field_dict["extensions"] = extensions
        if formatters is not UNSET:
            field_dict["formatters"] = formatters
        if functions is not UNSET:
            field_dict["functions"] = functions
        if keep_alive is not UNSET:
            field_dict["keepAlive"] = keep_alive
        if language_guessers is not UNSET:
            field_dict["languageGuessers"] = language_guessers
        if languages is not UNSET:
            field_dict["languages"] = languages
        if name is not UNSET:
            field_dict["name"] = name
        if natures is not UNSET:
            field_dict["natures"] = natures
        if operations is not UNSET:
            field_dict["operations"] = operations
        if processors is not UNSET:
            field_dict["processors"] = processors
        if segmenters is not UNSET:
            field_dict["segmenters"] = segmenters
        if service is not UNSET:
            field_dict["service"] = service
        if term_importers is not UNSET:
            field_dict["termImporters"] = term_importers
        if trigger is not UNSET:
            field_dict["trigger"] = trigger
        if vectorizers is not UNSET:
            field_dict["vectorizers"] = vectorizers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.http_service_metadata_operations import HttpServiceMetadataOperations
        from ..models.http_service_metadata_service import HttpServiceMetadataService

        d = src_dict.copy()
        api = d.pop("api")

        compatibility = d.pop("compatibility")

        version = d.pop("version")

        annotators = d.pop("annotators", UNSET)

        converters = d.pop("converters", UNSET)

        engine = d.pop("engine", UNSET)

        extensions = d.pop("extensions", UNSET)

        formatters = d.pop("formatters", UNSET)

        functions = d.pop("functions", UNSET)

        keep_alive = d.pop("keepAlive", UNSET)

        language_guessers = d.pop("languageGuessers", UNSET)

        languages = d.pop("languages", UNSET)

        name = d.pop("name", UNSET)

        natures = d.pop("natures", UNSET)

        _operations = d.pop("operations", UNSET)
        operations: Union[Unset, HttpServiceMetadataOperations]
        if isinstance(_operations, Unset):
            operations = UNSET
        else:
            operations = HttpServiceMetadataOperations.from_dict(_operations)

        processors = d.pop("processors", UNSET)

        segmenters = d.pop("segmenters", UNSET)

        _service = d.pop("service", UNSET)
        service: Union[Unset, HttpServiceMetadataService]
        if isinstance(_service, Unset):
            service = UNSET
        else:
            service = HttpServiceMetadataService.from_dict(_service)

        term_importers = d.pop("termImporters", UNSET)

        trigger = d.pop("trigger", UNSET)

        vectorizers = d.pop("vectorizers", UNSET)

        http_service_metadata = cls(
            api=api,
            compatibility=compatibility,
            version=version,
            annotators=annotators,
            converters=converters,
            engine=engine,
            extensions=extensions,
            formatters=formatters,
            functions=functions,
            keep_alive=keep_alive,
            language_guessers=language_guessers,
            languages=languages,
            name=name,
            natures=natures,
            operations=operations,
            processors=processors,
            segmenters=segmenters,
            service=service,
            term_importers=term_importers,
            trigger=trigger,
            vectorizers=vectorizers,
        )

        return http_service_metadata

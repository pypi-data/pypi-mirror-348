from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_service_record import HttpServiceRecord
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    name: Union[Unset, str] = "",
    api: Union[Unset, str] = "",
    keep_alive: Union[Unset, bool] = UNSET,
    engine: Union[Unset, str] = "",
    function: Union[Unset, str] = "",
    language: Union[Unset, str] = "",
    type_: Union[Unset, str] = "",
    nature: Union[Unset, str] = "",
    version: Union[Unset, str] = "",
    term_importer: Union[Unset, str] = "",
    annotator: Union[Unset, str] = "",
    processor: Union[Unset, str] = "",
    formatter: Union[Unset, str] = "",
    converter: Union[Unset, str] = "",
    segmenter: Union[Unset, str] = "",
    vectorizer: Union[Unset, str] = "",
    language_guesser: Union[Unset, str] = "",
    include_embedded_services: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["name"] = name

    params["api"] = api

    params["keepAlive"] = keep_alive

    params["engine"] = engine

    params["function"] = function

    params["language"] = language

    params["type"] = type_

    params["nature"] = nature

    params["version"] = version

    params["termImporter"] = term_importer

    params["annotator"] = annotator

    params["processor"] = processor

    params["formatter"] = formatter

    params["converter"] = converter

    params["segmenter"] = segmenter

    params["vectorizer"] = vectorizer

    params["languageGuesser"] = language_guesser

    params["includeEmbeddedServices"] = include_embedded_services

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/services",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["HttpServiceRecord"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_http_service_record_array_item_data in _response_200:
            componentsschemas_http_service_record_array_item = (
                HttpServiceRecord.from_dict(
                    componentsschemas_http_service_record_array_item_data
                )
            )

            response_200.append(componentsschemas_http_service_record_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["HttpServiceRecord"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = "",
    api: Union[Unset, str] = "",
    keep_alive: Union[Unset, bool] = UNSET,
    engine: Union[Unset, str] = "",
    function: Union[Unset, str] = "",
    language: Union[Unset, str] = "",
    type_: Union[Unset, str] = "",
    nature: Union[Unset, str] = "",
    version: Union[Unset, str] = "",
    term_importer: Union[Unset, str] = "",
    annotator: Union[Unset, str] = "",
    processor: Union[Unset, str] = "",
    formatter: Union[Unset, str] = "",
    converter: Union[Unset, str] = "",
    segmenter: Union[Unset, str] = "",
    vectorizer: Union[Unset, str] = "",
    language_guesser: Union[Unset, str] = "",
    include_embedded_services: Union[Unset, bool] = False,
) -> Response[list["HttpServiceRecord"]]:
    """Filter the list of available services

    Args:
        name (Union[Unset, str]):  Default: ''.
        api (Union[Unset, str]):  Default: ''.
        keep_alive (Union[Unset, bool]):
        engine (Union[Unset, str]):  Default: ''.
        function (Union[Unset, str]):  Default: ''.
        language (Union[Unset, str]):  Default: ''.
        type_ (Union[Unset, str]):  Default: ''.
        nature (Union[Unset, str]):  Default: ''.
        version (Union[Unset, str]):  Default: ''.
        term_importer (Union[Unset, str]):  Default: ''.
        annotator (Union[Unset, str]):  Default: ''.
        processor (Union[Unset, str]):  Default: ''.
        formatter (Union[Unset, str]):  Default: ''.
        converter (Union[Unset, str]):  Default: ''.
        segmenter (Union[Unset, str]):  Default: ''.
        vectorizer (Union[Unset, str]):  Default: ''.
        language_guesser (Union[Unset, str]):  Default: ''.
        include_embedded_services (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['HttpServiceRecord']]
    """

    kwargs = _get_kwargs(
        name=name,
        api=api,
        keep_alive=keep_alive,
        engine=engine,
        function=function,
        language=language,
        type_=type_,
        nature=nature,
        version=version,
        term_importer=term_importer,
        annotator=annotator,
        processor=processor,
        formatter=formatter,
        converter=converter,
        segmenter=segmenter,
        vectorizer=vectorizer,
        language_guesser=language_guesser,
        include_embedded_services=include_embedded_services,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = "",
    api: Union[Unset, str] = "",
    keep_alive: Union[Unset, bool] = UNSET,
    engine: Union[Unset, str] = "",
    function: Union[Unset, str] = "",
    language: Union[Unset, str] = "",
    type_: Union[Unset, str] = "",
    nature: Union[Unset, str] = "",
    version: Union[Unset, str] = "",
    term_importer: Union[Unset, str] = "",
    annotator: Union[Unset, str] = "",
    processor: Union[Unset, str] = "",
    formatter: Union[Unset, str] = "",
    converter: Union[Unset, str] = "",
    segmenter: Union[Unset, str] = "",
    vectorizer: Union[Unset, str] = "",
    language_guesser: Union[Unset, str] = "",
    include_embedded_services: Union[Unset, bool] = False,
) -> Optional[list["HttpServiceRecord"]]:
    """Filter the list of available services

    Args:
        name (Union[Unset, str]):  Default: ''.
        api (Union[Unset, str]):  Default: ''.
        keep_alive (Union[Unset, bool]):
        engine (Union[Unset, str]):  Default: ''.
        function (Union[Unset, str]):  Default: ''.
        language (Union[Unset, str]):  Default: ''.
        type_ (Union[Unset, str]):  Default: ''.
        nature (Union[Unset, str]):  Default: ''.
        version (Union[Unset, str]):  Default: ''.
        term_importer (Union[Unset, str]):  Default: ''.
        annotator (Union[Unset, str]):  Default: ''.
        processor (Union[Unset, str]):  Default: ''.
        formatter (Union[Unset, str]):  Default: ''.
        converter (Union[Unset, str]):  Default: ''.
        segmenter (Union[Unset, str]):  Default: ''.
        vectorizer (Union[Unset, str]):  Default: ''.
        language_guesser (Union[Unset, str]):  Default: ''.
        include_embedded_services (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['HttpServiceRecord']
    """

    return sync_detailed(
        client=client,
        name=name,
        api=api,
        keep_alive=keep_alive,
        engine=engine,
        function=function,
        language=language,
        type_=type_,
        nature=nature,
        version=version,
        term_importer=term_importer,
        annotator=annotator,
        processor=processor,
        formatter=formatter,
        converter=converter,
        segmenter=segmenter,
        vectorizer=vectorizer,
        language_guesser=language_guesser,
        include_embedded_services=include_embedded_services,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = "",
    api: Union[Unset, str] = "",
    keep_alive: Union[Unset, bool] = UNSET,
    engine: Union[Unset, str] = "",
    function: Union[Unset, str] = "",
    language: Union[Unset, str] = "",
    type_: Union[Unset, str] = "",
    nature: Union[Unset, str] = "",
    version: Union[Unset, str] = "",
    term_importer: Union[Unset, str] = "",
    annotator: Union[Unset, str] = "",
    processor: Union[Unset, str] = "",
    formatter: Union[Unset, str] = "",
    converter: Union[Unset, str] = "",
    segmenter: Union[Unset, str] = "",
    vectorizer: Union[Unset, str] = "",
    language_guesser: Union[Unset, str] = "",
    include_embedded_services: Union[Unset, bool] = False,
) -> Response[list["HttpServiceRecord"]]:
    """Filter the list of available services

    Args:
        name (Union[Unset, str]):  Default: ''.
        api (Union[Unset, str]):  Default: ''.
        keep_alive (Union[Unset, bool]):
        engine (Union[Unset, str]):  Default: ''.
        function (Union[Unset, str]):  Default: ''.
        language (Union[Unset, str]):  Default: ''.
        type_ (Union[Unset, str]):  Default: ''.
        nature (Union[Unset, str]):  Default: ''.
        version (Union[Unset, str]):  Default: ''.
        term_importer (Union[Unset, str]):  Default: ''.
        annotator (Union[Unset, str]):  Default: ''.
        processor (Union[Unset, str]):  Default: ''.
        formatter (Union[Unset, str]):  Default: ''.
        converter (Union[Unset, str]):  Default: ''.
        segmenter (Union[Unset, str]):  Default: ''.
        vectorizer (Union[Unset, str]):  Default: ''.
        language_guesser (Union[Unset, str]):  Default: ''.
        include_embedded_services (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['HttpServiceRecord']]
    """

    kwargs = _get_kwargs(
        name=name,
        api=api,
        keep_alive=keep_alive,
        engine=engine,
        function=function,
        language=language,
        type_=type_,
        nature=nature,
        version=version,
        term_importer=term_importer,
        annotator=annotator,
        processor=processor,
        formatter=formatter,
        converter=converter,
        segmenter=segmenter,
        vectorizer=vectorizer,
        language_guesser=language_guesser,
        include_embedded_services=include_embedded_services,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = "",
    api: Union[Unset, str] = "",
    keep_alive: Union[Unset, bool] = UNSET,
    engine: Union[Unset, str] = "",
    function: Union[Unset, str] = "",
    language: Union[Unset, str] = "",
    type_: Union[Unset, str] = "",
    nature: Union[Unset, str] = "",
    version: Union[Unset, str] = "",
    term_importer: Union[Unset, str] = "",
    annotator: Union[Unset, str] = "",
    processor: Union[Unset, str] = "",
    formatter: Union[Unset, str] = "",
    converter: Union[Unset, str] = "",
    segmenter: Union[Unset, str] = "",
    vectorizer: Union[Unset, str] = "",
    language_guesser: Union[Unset, str] = "",
    include_embedded_services: Union[Unset, bool] = False,
) -> Optional[list["HttpServiceRecord"]]:
    """Filter the list of available services

    Args:
        name (Union[Unset, str]):  Default: ''.
        api (Union[Unset, str]):  Default: ''.
        keep_alive (Union[Unset, bool]):
        engine (Union[Unset, str]):  Default: ''.
        function (Union[Unset, str]):  Default: ''.
        language (Union[Unset, str]):  Default: ''.
        type_ (Union[Unset, str]):  Default: ''.
        nature (Union[Unset, str]):  Default: ''.
        version (Union[Unset, str]):  Default: ''.
        term_importer (Union[Unset, str]):  Default: ''.
        annotator (Union[Unset, str]):  Default: ''.
        processor (Union[Unset, str]):  Default: ''.
        formatter (Union[Unset, str]):  Default: ''.
        converter (Union[Unset, str]):  Default: ''.
        segmenter (Union[Unset, str]):  Default: ''.
        vectorizer (Union[Unset, str]):  Default: ''.
        language_guesser (Union[Unset, str]):  Default: ''.
        include_embedded_services (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['HttpServiceRecord']
    """

    return (
        await asyncio_detailed(
            client=client,
            name=name,
            api=api,
            keep_alive=keep_alive,
            engine=engine,
            function=function,
            language=language,
            type_=type_,
            nature=nature,
            version=version,
            term_importer=term_importer,
            annotator=annotator,
            processor=processor,
            formatter=formatter,
            converter=converter,
            segmenter=segmenter,
            vectorizer=vectorizer,
            language_guesser=language_guesser,
            include_embedded_services=include_embedded_services,
        )
    ).parsed

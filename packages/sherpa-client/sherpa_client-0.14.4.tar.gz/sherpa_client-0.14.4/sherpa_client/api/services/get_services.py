from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.http_service_record import HttpServiceRecord
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    name: Union[Unset, None, str] = "",
    api: Union[Unset, None, str] = "",
    keep_alive: Union[Unset, None, bool] = UNSET,
    engine: Union[Unset, None, str] = "",
    function: Union[Unset, None, str] = "",
    language: Union[Unset, None, str] = "",
    type: Union[Unset, None, str] = "",
    nature: Union[Unset, None, str] = "",
    version: Union[Unset, None, str] = "",
    term_importer: Union[Unset, None, str] = "",
    annotator: Union[Unset, None, str] = "",
    processor: Union[Unset, None, str] = "",
    formatter: Union[Unset, None, str] = "",
    converter: Union[Unset, None, str] = "",
    segmenter: Union[Unset, None, str] = "",
    vectorizer: Union[Unset, None, str] = "",
    language_guesser: Union[Unset, None, str] = "",
    include_embedded_services: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/services".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["name"] = name

    params["api"] = api

    params["keepAlive"] = keep_alive

    params["engine"] = engine

    params["function"] = function

    params["language"] = language

    params["type"] = type

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

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[List["HttpServiceRecord"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_http_service_record_array_item_data in _response_200:
            componentsschemas_http_service_record_array_item = HttpServiceRecord.from_dict(
                componentsschemas_http_service_record_array_item_data
            )

            response_200.append(componentsschemas_http_service_record_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[List["HttpServiceRecord"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    name: Union[Unset, None, str] = "",
    api: Union[Unset, None, str] = "",
    keep_alive: Union[Unset, None, bool] = UNSET,
    engine: Union[Unset, None, str] = "",
    function: Union[Unset, None, str] = "",
    language: Union[Unset, None, str] = "",
    type: Union[Unset, None, str] = "",
    nature: Union[Unset, None, str] = "",
    version: Union[Unset, None, str] = "",
    term_importer: Union[Unset, None, str] = "",
    annotator: Union[Unset, None, str] = "",
    processor: Union[Unset, None, str] = "",
    formatter: Union[Unset, None, str] = "",
    converter: Union[Unset, None, str] = "",
    segmenter: Union[Unset, None, str] = "",
    vectorizer: Union[Unset, None, str] = "",
    language_guesser: Union[Unset, None, str] = "",
    include_embedded_services: Union[Unset, None, bool] = False,
) -> Response[List["HttpServiceRecord"]]:
    """Filter the list of available services

    Args:
        name (Union[Unset, None, str]):  Default: ''.
        api (Union[Unset, None, str]):  Default: ''.
        keep_alive (Union[Unset, None, bool]):
        engine (Union[Unset, None, str]):  Default: ''.
        function (Union[Unset, None, str]):  Default: ''.
        language (Union[Unset, None, str]):  Default: ''.
        type (Union[Unset, None, str]):  Default: ''.
        nature (Union[Unset, None, str]):  Default: ''.
        version (Union[Unset, None, str]):  Default: ''.
        term_importer (Union[Unset, None, str]):  Default: ''.
        annotator (Union[Unset, None, str]):  Default: ''.
        processor (Union[Unset, None, str]):  Default: ''.
        formatter (Union[Unset, None, str]):  Default: ''.
        converter (Union[Unset, None, str]):  Default: ''.
        segmenter (Union[Unset, None, str]):  Default: ''.
        vectorizer (Union[Unset, None, str]):  Default: ''.
        language_guesser (Union[Unset, None, str]):  Default: ''.
        include_embedded_services (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['HttpServiceRecord']]
    """

    kwargs = _get_kwargs(
        client=client,
        name=name,
        api=api,
        keep_alive=keep_alive,
        engine=engine,
        function=function,
        language=language,
        type=type,
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

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    name: Union[Unset, None, str] = "",
    api: Union[Unset, None, str] = "",
    keep_alive: Union[Unset, None, bool] = UNSET,
    engine: Union[Unset, None, str] = "",
    function: Union[Unset, None, str] = "",
    language: Union[Unset, None, str] = "",
    type: Union[Unset, None, str] = "",
    nature: Union[Unset, None, str] = "",
    version: Union[Unset, None, str] = "",
    term_importer: Union[Unset, None, str] = "",
    annotator: Union[Unset, None, str] = "",
    processor: Union[Unset, None, str] = "",
    formatter: Union[Unset, None, str] = "",
    converter: Union[Unset, None, str] = "",
    segmenter: Union[Unset, None, str] = "",
    vectorizer: Union[Unset, None, str] = "",
    language_guesser: Union[Unset, None, str] = "",
    include_embedded_services: Union[Unset, None, bool] = False,
) -> Optional[List["HttpServiceRecord"]]:
    """Filter the list of available services

    Args:
        name (Union[Unset, None, str]):  Default: ''.
        api (Union[Unset, None, str]):  Default: ''.
        keep_alive (Union[Unset, None, bool]):
        engine (Union[Unset, None, str]):  Default: ''.
        function (Union[Unset, None, str]):  Default: ''.
        language (Union[Unset, None, str]):  Default: ''.
        type (Union[Unset, None, str]):  Default: ''.
        nature (Union[Unset, None, str]):  Default: ''.
        version (Union[Unset, None, str]):  Default: ''.
        term_importer (Union[Unset, None, str]):  Default: ''.
        annotator (Union[Unset, None, str]):  Default: ''.
        processor (Union[Unset, None, str]):  Default: ''.
        formatter (Union[Unset, None, str]):  Default: ''.
        converter (Union[Unset, None, str]):  Default: ''.
        segmenter (Union[Unset, None, str]):  Default: ''.
        vectorizer (Union[Unset, None, str]):  Default: ''.
        language_guesser (Union[Unset, None, str]):  Default: ''.
        include_embedded_services (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['HttpServiceRecord']]
    """

    return sync_detailed(
        client=client,
        name=name,
        api=api,
        keep_alive=keep_alive,
        engine=engine,
        function=function,
        language=language,
        type=type,
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
    client: Client,
    name: Union[Unset, None, str] = "",
    api: Union[Unset, None, str] = "",
    keep_alive: Union[Unset, None, bool] = UNSET,
    engine: Union[Unset, None, str] = "",
    function: Union[Unset, None, str] = "",
    language: Union[Unset, None, str] = "",
    type: Union[Unset, None, str] = "",
    nature: Union[Unset, None, str] = "",
    version: Union[Unset, None, str] = "",
    term_importer: Union[Unset, None, str] = "",
    annotator: Union[Unset, None, str] = "",
    processor: Union[Unset, None, str] = "",
    formatter: Union[Unset, None, str] = "",
    converter: Union[Unset, None, str] = "",
    segmenter: Union[Unset, None, str] = "",
    vectorizer: Union[Unset, None, str] = "",
    language_guesser: Union[Unset, None, str] = "",
    include_embedded_services: Union[Unset, None, bool] = False,
) -> Response[List["HttpServiceRecord"]]:
    """Filter the list of available services

    Args:
        name (Union[Unset, None, str]):  Default: ''.
        api (Union[Unset, None, str]):  Default: ''.
        keep_alive (Union[Unset, None, bool]):
        engine (Union[Unset, None, str]):  Default: ''.
        function (Union[Unset, None, str]):  Default: ''.
        language (Union[Unset, None, str]):  Default: ''.
        type (Union[Unset, None, str]):  Default: ''.
        nature (Union[Unset, None, str]):  Default: ''.
        version (Union[Unset, None, str]):  Default: ''.
        term_importer (Union[Unset, None, str]):  Default: ''.
        annotator (Union[Unset, None, str]):  Default: ''.
        processor (Union[Unset, None, str]):  Default: ''.
        formatter (Union[Unset, None, str]):  Default: ''.
        converter (Union[Unset, None, str]):  Default: ''.
        segmenter (Union[Unset, None, str]):  Default: ''.
        vectorizer (Union[Unset, None, str]):  Default: ''.
        language_guesser (Union[Unset, None, str]):  Default: ''.
        include_embedded_services (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['HttpServiceRecord']]
    """

    kwargs = _get_kwargs(
        client=client,
        name=name,
        api=api,
        keep_alive=keep_alive,
        engine=engine,
        function=function,
        language=language,
        type=type,
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

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    name: Union[Unset, None, str] = "",
    api: Union[Unset, None, str] = "",
    keep_alive: Union[Unset, None, bool] = UNSET,
    engine: Union[Unset, None, str] = "",
    function: Union[Unset, None, str] = "",
    language: Union[Unset, None, str] = "",
    type: Union[Unset, None, str] = "",
    nature: Union[Unset, None, str] = "",
    version: Union[Unset, None, str] = "",
    term_importer: Union[Unset, None, str] = "",
    annotator: Union[Unset, None, str] = "",
    processor: Union[Unset, None, str] = "",
    formatter: Union[Unset, None, str] = "",
    converter: Union[Unset, None, str] = "",
    segmenter: Union[Unset, None, str] = "",
    vectorizer: Union[Unset, None, str] = "",
    language_guesser: Union[Unset, None, str] = "",
    include_embedded_services: Union[Unset, None, bool] = False,
) -> Optional[List["HttpServiceRecord"]]:
    """Filter the list of available services

    Args:
        name (Union[Unset, None, str]):  Default: ''.
        api (Union[Unset, None, str]):  Default: ''.
        keep_alive (Union[Unset, None, bool]):
        engine (Union[Unset, None, str]):  Default: ''.
        function (Union[Unset, None, str]):  Default: ''.
        language (Union[Unset, None, str]):  Default: ''.
        type (Union[Unset, None, str]):  Default: ''.
        nature (Union[Unset, None, str]):  Default: ''.
        version (Union[Unset, None, str]):  Default: ''.
        term_importer (Union[Unset, None, str]):  Default: ''.
        annotator (Union[Unset, None, str]):  Default: ''.
        processor (Union[Unset, None, str]):  Default: ''.
        formatter (Union[Unset, None, str]):  Default: ''.
        converter (Union[Unset, None, str]):  Default: ''.
        segmenter (Union[Unset, None, str]):  Default: ''.
        vectorizer (Union[Unset, None, str]):  Default: ''.
        language_guesser (Union[Unset, None, str]):  Default: ''.
        include_embedded_services (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['HttpServiceRecord']]
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
            type=type,
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

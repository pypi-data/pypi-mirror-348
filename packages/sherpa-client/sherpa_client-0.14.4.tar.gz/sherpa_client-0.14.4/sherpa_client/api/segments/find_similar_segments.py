from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.find_similar_segments_search_type import FindSimilarSegmentsSearchType
from ...models.segment_hits import SegmentHits
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    segid: Union[Unset, None, str] = "",
    text: Union[Unset, None, str] = "",
    fields: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    search_type: Union[Unset, None, FindSimilarSegmentsSearchType] = FindSimilarSegmentsSearchType.TEXT,
    native_rrf: Union[Unset, None, bool] = UNSET,
    vectorizer: Union[Unset, None, str] = UNSET,
    vector_query: Union[Unset, None, str] = "",
    html_version: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/segments/_similar".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["segid"] = segid

    params["text"] = text

    params["fields"] = fields

    params["from"] = from_

    params["size"] = size

    params["highlight"] = highlight

    params["facet"] = facet

    params["queryFilter"] = query_filter

    params["outputFields"] = output_fields

    params["simpleQuery"] = simple_query

    json_selected_facets: Union[Unset, None, List[str]] = UNSET
    if not isinstance(selected_facets, Unset):
        if selected_facets is None:
            json_selected_facets = None
        else:
            json_selected_facets = selected_facets

    params["selectedFacets"] = json_selected_facets

    params["invertSearch"] = invert_search

    json_search_type: Union[Unset, None, str] = UNSET
    if not isinstance(search_type, Unset):
        json_search_type = search_type.value if search_type else None

    params["searchType"] = json_search_type

    params["nativeRRF"] = native_rrf

    params["vectorizer"] = vectorizer

    params["vectorQuery"] = vector_query

    params["htmlVersion"] = html_version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[SegmentHits]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SegmentHits.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[SegmentHits]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    *,
    client: Client,
    segid: Union[Unset, None, str] = "",
    text: Union[Unset, None, str] = "",
    fields: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    search_type: Union[Unset, None, FindSimilarSegmentsSearchType] = FindSimilarSegmentsSearchType.TEXT,
    native_rrf: Union[Unset, None, bool] = UNSET,
    vectorizer: Union[Unset, None, str] = UNSET,
    vector_query: Union[Unset, None, str] = "",
    html_version: Union[Unset, None, bool] = False,
) -> Response[SegmentHits]:
    """Search for similar segments

    Args:
        project_name (str):
        segid (Union[Unset, None, str]):  Default: ''.
        text (Union[Unset, None, str]):  Default: ''.
        fields (Union[Unset, None, str]):  Default: ''.
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 10.
        highlight (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):
        query_filter (Union[Unset, None, str]):  Default: ''.
        output_fields (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        invert_search (Union[Unset, None, bool]):
        search_type (Union[Unset, None, FindSimilarSegmentsSearchType]):  Default:
            FindSimilarSegmentsSearchType.TEXT.
        native_rrf (Union[Unset, None, bool]):
        vectorizer (Union[Unset, None, str]):
        vector_query (Union[Unset, None, str]):  Default: ''.
        html_version (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SegmentHits]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        segid=segid,
        text=text,
        fields=fields,
        from_=from_,
        size=size,
        highlight=highlight,
        facet=facet,
        query_filter=query_filter,
        output_fields=output_fields,
        simple_query=simple_query,
        selected_facets=selected_facets,
        invert_search=invert_search,
        search_type=search_type,
        native_rrf=native_rrf,
        vectorizer=vectorizer,
        vector_query=vector_query,
        html_version=html_version,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Client,
    segid: Union[Unset, None, str] = "",
    text: Union[Unset, None, str] = "",
    fields: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    search_type: Union[Unset, None, FindSimilarSegmentsSearchType] = FindSimilarSegmentsSearchType.TEXT,
    native_rrf: Union[Unset, None, bool] = UNSET,
    vectorizer: Union[Unset, None, str] = UNSET,
    vector_query: Union[Unset, None, str] = "",
    html_version: Union[Unset, None, bool] = False,
) -> Optional[SegmentHits]:
    """Search for similar segments

    Args:
        project_name (str):
        segid (Union[Unset, None, str]):  Default: ''.
        text (Union[Unset, None, str]):  Default: ''.
        fields (Union[Unset, None, str]):  Default: ''.
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 10.
        highlight (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):
        query_filter (Union[Unset, None, str]):  Default: ''.
        output_fields (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        invert_search (Union[Unset, None, bool]):
        search_type (Union[Unset, None, FindSimilarSegmentsSearchType]):  Default:
            FindSimilarSegmentsSearchType.TEXT.
        native_rrf (Union[Unset, None, bool]):
        vectorizer (Union[Unset, None, str]):
        vector_query (Union[Unset, None, str]):  Default: ''.
        html_version (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SegmentHits]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        segid=segid,
        text=text,
        fields=fields,
        from_=from_,
        size=size,
        highlight=highlight,
        facet=facet,
        query_filter=query_filter,
        output_fields=output_fields,
        simple_query=simple_query,
        selected_facets=selected_facets,
        invert_search=invert_search,
        search_type=search_type,
        native_rrf=native_rrf,
        vectorizer=vectorizer,
        vector_query=vector_query,
        html_version=html_version,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    segid: Union[Unset, None, str] = "",
    text: Union[Unset, None, str] = "",
    fields: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    search_type: Union[Unset, None, FindSimilarSegmentsSearchType] = FindSimilarSegmentsSearchType.TEXT,
    native_rrf: Union[Unset, None, bool] = UNSET,
    vectorizer: Union[Unset, None, str] = UNSET,
    vector_query: Union[Unset, None, str] = "",
    html_version: Union[Unset, None, bool] = False,
) -> Response[SegmentHits]:
    """Search for similar segments

    Args:
        project_name (str):
        segid (Union[Unset, None, str]):  Default: ''.
        text (Union[Unset, None, str]):  Default: ''.
        fields (Union[Unset, None, str]):  Default: ''.
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 10.
        highlight (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):
        query_filter (Union[Unset, None, str]):  Default: ''.
        output_fields (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        invert_search (Union[Unset, None, bool]):
        search_type (Union[Unset, None, FindSimilarSegmentsSearchType]):  Default:
            FindSimilarSegmentsSearchType.TEXT.
        native_rrf (Union[Unset, None, bool]):
        vectorizer (Union[Unset, None, str]):
        vector_query (Union[Unset, None, str]):  Default: ''.
        html_version (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SegmentHits]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        segid=segid,
        text=text,
        fields=fields,
        from_=from_,
        size=size,
        highlight=highlight,
        facet=facet,
        query_filter=query_filter,
        output_fields=output_fields,
        simple_query=simple_query,
        selected_facets=selected_facets,
        invert_search=invert_search,
        search_type=search_type,
        native_rrf=native_rrf,
        vectorizer=vectorizer,
        vector_query=vector_query,
        html_version=html_version,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    segid: Union[Unset, None, str] = "",
    text: Union[Unset, None, str] = "",
    fields: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    search_type: Union[Unset, None, FindSimilarSegmentsSearchType] = FindSimilarSegmentsSearchType.TEXT,
    native_rrf: Union[Unset, None, bool] = UNSET,
    vectorizer: Union[Unset, None, str] = UNSET,
    vector_query: Union[Unset, None, str] = "",
    html_version: Union[Unset, None, bool] = False,
) -> Optional[SegmentHits]:
    """Search for similar segments

    Args:
        project_name (str):
        segid (Union[Unset, None, str]):  Default: ''.
        text (Union[Unset, None, str]):  Default: ''.
        fields (Union[Unset, None, str]):  Default: ''.
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 10.
        highlight (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):
        query_filter (Union[Unset, None, str]):  Default: ''.
        output_fields (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        invert_search (Union[Unset, None, bool]):
        search_type (Union[Unset, None, FindSimilarSegmentsSearchType]):  Default:
            FindSimilarSegmentsSearchType.TEXT.
        native_rrf (Union[Unset, None, bool]):
        vectorizer (Union[Unset, None, str]):
        vector_query (Union[Unset, None, str]):  Default: ''.
        html_version (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SegmentHits]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            segid=segid,
            text=text,
            fields=fields,
            from_=from_,
            size=size,
            highlight=highlight,
            facet=facet,
            query_filter=query_filter,
            output_fields=output_fields,
            simple_query=simple_query,
            selected_facets=selected_facets,
            invert_search=invert_search,
            search_type=search_type,
            native_rrf=native_rrf,
            vectorizer=vectorizer,
            vector_query=vector_query,
            html_version=html_version,
        )
    ).parsed

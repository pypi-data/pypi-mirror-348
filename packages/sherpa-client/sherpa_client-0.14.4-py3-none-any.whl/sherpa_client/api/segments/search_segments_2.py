from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.search_request import SearchRequest
from ...models.segment_hits import SegmentHits
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    json_body: SearchRequest,
    saved_search: Union[Unset, None, str] = UNSET,
    default_saved_search: Union[Unset, None, bool] = False,
    html_version: Union[Unset, None, bool] = False,
    async_answer: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/segments/_do_search".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["savedSearch"] = saved_search

    params["defaultSavedSearch"] = default_saved_search

    params["htmlVersion"] = html_version

    params["asyncAnswer"] = async_answer

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
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
    json_body: SearchRequest,
    saved_search: Union[Unset, None, str] = UNSET,
    default_saved_search: Union[Unset, None, bool] = False,
    html_version: Union[Unset, None, bool] = False,
    async_answer: Union[Unset, None, bool] = False,
) -> Response[SegmentHits]:
    """Search for segments

    Args:
        project_name (str):
        saved_search (Union[Unset, None, str]):
        default_saved_search (Union[Unset, None, bool]):
        html_version (Union[Unset, None, bool]):
        async_answer (Union[Unset, None, bool]):
        json_body (SearchRequest): Search request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SegmentHits]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        json_body=json_body,
        saved_search=saved_search,
        default_saved_search=default_saved_search,
        html_version=html_version,
        async_answer=async_answer,
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
    json_body: SearchRequest,
    saved_search: Union[Unset, None, str] = UNSET,
    default_saved_search: Union[Unset, None, bool] = False,
    html_version: Union[Unset, None, bool] = False,
    async_answer: Union[Unset, None, bool] = False,
) -> Optional[SegmentHits]:
    """Search for segments

    Args:
        project_name (str):
        saved_search (Union[Unset, None, str]):
        default_saved_search (Union[Unset, None, bool]):
        html_version (Union[Unset, None, bool]):
        async_answer (Union[Unset, None, bool]):
        json_body (SearchRequest): Search request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SegmentHits]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        json_body=json_body,
        saved_search=saved_search,
        default_saved_search=default_saved_search,
        html_version=html_version,
        async_answer=async_answer,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    json_body: SearchRequest,
    saved_search: Union[Unset, None, str] = UNSET,
    default_saved_search: Union[Unset, None, bool] = False,
    html_version: Union[Unset, None, bool] = False,
    async_answer: Union[Unset, None, bool] = False,
) -> Response[SegmentHits]:
    """Search for segments

    Args:
        project_name (str):
        saved_search (Union[Unset, None, str]):
        default_saved_search (Union[Unset, None, bool]):
        html_version (Union[Unset, None, bool]):
        async_answer (Union[Unset, None, bool]):
        json_body (SearchRequest): Search request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SegmentHits]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        json_body=json_body,
        saved_search=saved_search,
        default_saved_search=default_saved_search,
        html_version=html_version,
        async_answer=async_answer,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    json_body: SearchRequest,
    saved_search: Union[Unset, None, str] = UNSET,
    default_saved_search: Union[Unset, None, bool] = False,
    html_version: Union[Unset, None, bool] = False,
    async_answer: Union[Unset, None, bool] = False,
) -> Optional[SegmentHits]:
    """Search for segments

    Args:
        project_name (str):
        saved_search (Union[Unset, None, str]):
        default_saved_search (Union[Unset, None, bool]):
        html_version (Union[Unset, None, bool]):
        async_answer (Union[Unset, None, bool]):
        json_body (SearchRequest): Search request

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
            json_body=json_body,
            saved_search=saved_search,
            default_saved_search=default_saved_search,
            html_version=html_version,
            async_answer=async_answer,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_request import SearchRequest
from ...models.segment_hits import SegmentHits
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    body: SearchRequest,
    saved_search: Union[Unset, str] = UNSET,
    default_saved_search: Union[Unset, bool] = False,
    html_version: Union[Unset, bool] = False,
    async_answer: Union[Unset, bool] = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["savedSearch"] = saved_search

    params["defaultSavedSearch"] = default_saved_search

    params["htmlVersion"] = html_version

    params["asyncAnswer"] = async_answer

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/segments/_do_search".format(
            project_name=project_name,
        ),
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SegmentHits]:
    if response.status_code == 200:
        response_200 = SegmentHits.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SegmentHits]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SearchRequest,
    saved_search: Union[Unset, str] = UNSET,
    default_saved_search: Union[Unset, bool] = False,
    html_version: Union[Unset, bool] = False,
    async_answer: Union[Unset, bool] = False,
) -> Response[SegmentHits]:
    """Search for segments

    Args:
        project_name (str):
        saved_search (Union[Unset, str]):
        default_saved_search (Union[Unset, bool]):  Default: False.
        html_version (Union[Unset, bool]):  Default: False.
        async_answer (Union[Unset, bool]):  Default: False.
        body (SearchRequest): Search request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SegmentHits]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        body=body,
        saved_search=saved_search,
        default_saved_search=default_saved_search,
        html_version=html_version,
        async_answer=async_answer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SearchRequest,
    saved_search: Union[Unset, str] = UNSET,
    default_saved_search: Union[Unset, bool] = False,
    html_version: Union[Unset, bool] = False,
    async_answer: Union[Unset, bool] = False,
) -> Optional[SegmentHits]:
    """Search for segments

    Args:
        project_name (str):
        saved_search (Union[Unset, str]):
        default_saved_search (Union[Unset, bool]):  Default: False.
        html_version (Union[Unset, bool]):  Default: False.
        async_answer (Union[Unset, bool]):  Default: False.
        body (SearchRequest): Search request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SegmentHits
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        body=body,
        saved_search=saved_search,
        default_saved_search=default_saved_search,
        html_version=html_version,
        async_answer=async_answer,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SearchRequest,
    saved_search: Union[Unset, str] = UNSET,
    default_saved_search: Union[Unset, bool] = False,
    html_version: Union[Unset, bool] = False,
    async_answer: Union[Unset, bool] = False,
) -> Response[SegmentHits]:
    """Search for segments

    Args:
        project_name (str):
        saved_search (Union[Unset, str]):
        default_saved_search (Union[Unset, bool]):  Default: False.
        html_version (Union[Unset, bool]):  Default: False.
        async_answer (Union[Unset, bool]):  Default: False.
        body (SearchRequest): Search request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SegmentHits]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        body=body,
        saved_search=saved_search,
        default_saved_search=default_saved_search,
        html_version=html_version,
        async_answer=async_answer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SearchRequest,
    saved_search: Union[Unset, str] = UNSET,
    default_saved_search: Union[Unset, bool] = False,
    html_version: Union[Unset, bool] = False,
    async_answer: Union[Unset, bool] = False,
) -> Optional[SegmentHits]:
    """Search for segments

    Args:
        project_name (str):
        saved_search (Union[Unset, str]):
        default_saved_search (Union[Unset, bool]):  Default: False.
        html_version (Union[Unset, bool]):  Default: False.
        async_answer (Union[Unset, bool]):  Default: False.
        body (SearchRequest): Search request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SegmentHits
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            body=body,
            saved_search=saved_search,
            default_saved_search=default_saved_search,
            html_version=html_version,
            async_answer=async_answer,
        )
    ).parsed

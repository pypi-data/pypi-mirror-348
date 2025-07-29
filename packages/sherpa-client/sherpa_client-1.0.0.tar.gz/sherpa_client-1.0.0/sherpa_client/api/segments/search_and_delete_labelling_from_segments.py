from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sherpa_job_bean import SherpaJobBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    query: Union[Unset, str] = "",
    query_filter: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    labels: Union[Unset, list[str]] = UNSET,
    created_by: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["query"] = query

    params["queryFilter"] = query_filter

    params["simpleQuery"] = simple_query

    json_selected_facets: Union[Unset, list[str]] = UNSET
    if not isinstance(selected_facets, Unset):
        json_selected_facets = selected_facets

    params["selectedFacets"] = json_selected_facets

    params["invertSearch"] = invert_search

    json_labels: Union[Unset, list[str]] = UNSET
    if not isinstance(labels, Unset):
        json_labels = labels

    params["labels"] = json_labels

    json_created_by: Union[Unset, list[str]] = UNSET
    if not isinstance(created_by, Unset):
        json_created_by = created_by

    params["createdBy"] = json_created_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/segments/_search_and_delete_labelling".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SherpaJobBean]:
    if response.status_code == 200:
        response_200 = SherpaJobBean.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SherpaJobBean]:
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
    query: Union[Unset, str] = "",
    query_filter: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    labels: Union[Unset, list[str]] = UNSET,
    created_by: Union[Unset, list[str]] = UNSET,
) -> Response[SherpaJobBean]:
    """Search for segments and delete annotations from all of them

    Args:
        project_name (str):
        query (Union[Unset, str]):  Default: ''.
        query_filter (Union[Unset, str]):  Default: ''.
        simple_query (Union[Unset, bool]):  Default: False.
        selected_facets (Union[Unset, list[str]]):
        invert_search (Union[Unset, bool]):  Default: False.
        labels (Union[Unset, list[str]]):
        created_by (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        query=query,
        query_filter=query_filter,
        simple_query=simple_query,
        selected_facets=selected_facets,
        invert_search=invert_search,
        labels=labels,
        created_by=created_by,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    query_filter: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    labels: Union[Unset, list[str]] = UNSET,
    created_by: Union[Unset, list[str]] = UNSET,
) -> Optional[SherpaJobBean]:
    """Search for segments and delete annotations from all of them

    Args:
        project_name (str):
        query (Union[Unset, str]):  Default: ''.
        query_filter (Union[Unset, str]):  Default: ''.
        simple_query (Union[Unset, bool]):  Default: False.
        selected_facets (Union[Unset, list[str]]):
        invert_search (Union[Unset, bool]):  Default: False.
        labels (Union[Unset, list[str]]):
        created_by (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SherpaJobBean
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        query=query,
        query_filter=query_filter,
        simple_query=simple_query,
        selected_facets=selected_facets,
        invert_search=invert_search,
        labels=labels,
        created_by=created_by,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    query_filter: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    labels: Union[Unset, list[str]] = UNSET,
    created_by: Union[Unset, list[str]] = UNSET,
) -> Response[SherpaJobBean]:
    """Search for segments and delete annotations from all of them

    Args:
        project_name (str):
        query (Union[Unset, str]):  Default: ''.
        query_filter (Union[Unset, str]):  Default: ''.
        simple_query (Union[Unset, bool]):  Default: False.
        selected_facets (Union[Unset, list[str]]):
        invert_search (Union[Unset, bool]):  Default: False.
        labels (Union[Unset, list[str]]):
        created_by (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        query=query,
        query_filter=query_filter,
        simple_query=simple_query,
        selected_facets=selected_facets,
        invert_search=invert_search,
        labels=labels,
        created_by=created_by,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    query_filter: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    labels: Union[Unset, list[str]] = UNSET,
    created_by: Union[Unset, list[str]] = UNSET,
) -> Optional[SherpaJobBean]:
    """Search for segments and delete annotations from all of them

    Args:
        project_name (str):
        query (Union[Unset, str]):  Default: ''.
        query_filter (Union[Unset, str]):  Default: ''.
        simple_query (Union[Unset, bool]):  Default: False.
        selected_facets (Union[Unset, list[str]]):
        invert_search (Union[Unset, bool]):  Default: False.
        labels (Union[Unset, list[str]]):
        created_by (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SherpaJobBean
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            query=query,
            query_filter=query_filter,
            simple_query=simple_query,
            selected_facets=selected_facets,
            invert_search=invert_search,
            labels=labels,
            created_by=created_by,
        )
    ).parsed

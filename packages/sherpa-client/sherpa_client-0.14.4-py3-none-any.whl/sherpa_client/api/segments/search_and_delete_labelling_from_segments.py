from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.sherpa_job_bean import SherpaJobBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    query_filter: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    labels: Union[Unset, None, List[str]] = UNSET,
    created_by: Union[Unset, None, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/segments/_search_and_delete_labelling".format(
        client.base_url, projectName=project_name
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["query"] = query

    params["queryFilter"] = query_filter

    params["simpleQuery"] = simple_query

    json_selected_facets: Union[Unset, None, List[str]] = UNSET
    if not isinstance(selected_facets, Unset):
        if selected_facets is None:
            json_selected_facets = None
        else:
            json_selected_facets = selected_facets

    params["selectedFacets"] = json_selected_facets

    params["invertSearch"] = invert_search

    json_labels: Union[Unset, None, List[str]] = UNSET
    if not isinstance(labels, Unset):
        if labels is None:
            json_labels = None
        else:
            json_labels = labels

    params["labels"] = json_labels

    json_created_by: Union[Unset, None, List[str]] = UNSET
    if not isinstance(created_by, Unset):
        if created_by is None:
            json_created_by = None
        else:
            json_created_by = created_by

    params["createdBy"] = json_created_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[SherpaJobBean]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SherpaJobBean.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[SherpaJobBean]:
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
    query: Union[Unset, None, str] = "",
    query_filter: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    labels: Union[Unset, None, List[str]] = UNSET,
    created_by: Union[Unset, None, List[str]] = UNSET,
) -> Response[SherpaJobBean]:
    """Search for segments and delete annotations from all of them

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        query_filter (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        invert_search (Union[Unset, None, bool]):
        labels (Union[Unset, None, List[str]]):
        created_by (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
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

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    query_filter: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    labels: Union[Unset, None, List[str]] = UNSET,
    created_by: Union[Unset, None, List[str]] = UNSET,
) -> Optional[SherpaJobBean]:
    """Search for segments and delete annotations from all of them

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        query_filter (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        invert_search (Union[Unset, None, bool]):
        labels (Union[Unset, None, List[str]]):
        created_by (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
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
    client: Client,
    query: Union[Unset, None, str] = "",
    query_filter: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    labels: Union[Unset, None, List[str]] = UNSET,
    created_by: Union[Unset, None, List[str]] = UNSET,
) -> Response[SherpaJobBean]:
    """Search for segments and delete annotations from all of them

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        query_filter (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        invert_search (Union[Unset, None, bool]):
        labels (Union[Unset, None, List[str]]):
        created_by (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
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

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    query_filter: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    labels: Union[Unset, None, List[str]] = UNSET,
    created_by: Union[Unset, None, List[str]] = UNSET,
) -> Optional[SherpaJobBean]:
    """Search for segments and delete annotations from all of them

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        query_filter (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        invert_search (Union[Unset, None, bool]):
        labels (Union[Unset, None, List[str]]):
        created_by (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
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

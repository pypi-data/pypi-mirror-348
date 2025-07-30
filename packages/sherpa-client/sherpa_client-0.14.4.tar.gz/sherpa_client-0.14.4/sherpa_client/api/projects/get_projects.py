from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.project_bean import ProjectBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
    compute_owners: Union[Unset, None, bool] = False,
    compute_engines: Union[Unset, None, bool] = False,
    estimated_counts: Union[Unset, None, bool] = False,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/projects".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["computeMetrics"] = compute_metrics

    params["computeOwners"] = compute_owners

    params["computeEngines"] = compute_engines

    params["estimatedCounts"] = estimated_counts

    params["groupName"] = group_name

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[List["ProjectBean"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_project_bean_array_item_data in _response_200:
            componentsschemas_project_bean_array_item = ProjectBean.from_dict(
                componentsschemas_project_bean_array_item_data
            )

            response_200.append(componentsschemas_project_bean_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[List["ProjectBean"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
    compute_owners: Union[Unset, None, bool] = False,
    compute_engines: Union[Unset, None, bool] = False,
    estimated_counts: Union[Unset, None, bool] = False,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Response[List["ProjectBean"]]:
    """Get projects

    Args:
        compute_metrics (Union[Unset, None, bool]):
        compute_owners (Union[Unset, None, bool]):
        compute_engines (Union[Unset, None, bool]):
        estimated_counts (Union[Unset, None, bool]):
        group_name (Union[Unset, None, str]):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ProjectBean']]
    """

    kwargs = _get_kwargs(
        client=client,
        compute_metrics=compute_metrics,
        compute_owners=compute_owners,
        compute_engines=compute_engines,
        estimated_counts=estimated_counts,
        group_name=group_name,
        username=username,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
    compute_owners: Union[Unset, None, bool] = False,
    compute_engines: Union[Unset, None, bool] = False,
    estimated_counts: Union[Unset, None, bool] = False,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Optional[List["ProjectBean"]]:
    """Get projects

    Args:
        compute_metrics (Union[Unset, None, bool]):
        compute_owners (Union[Unset, None, bool]):
        compute_engines (Union[Unset, None, bool]):
        estimated_counts (Union[Unset, None, bool]):
        group_name (Union[Unset, None, str]):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ProjectBean']]
    """

    return sync_detailed(
        client=client,
        compute_metrics=compute_metrics,
        compute_owners=compute_owners,
        compute_engines=compute_engines,
        estimated_counts=estimated_counts,
        group_name=group_name,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
    compute_owners: Union[Unset, None, bool] = False,
    compute_engines: Union[Unset, None, bool] = False,
    estimated_counts: Union[Unset, None, bool] = False,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Response[List["ProjectBean"]]:
    """Get projects

    Args:
        compute_metrics (Union[Unset, None, bool]):
        compute_owners (Union[Unset, None, bool]):
        compute_engines (Union[Unset, None, bool]):
        estimated_counts (Union[Unset, None, bool]):
        group_name (Union[Unset, None, str]):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ProjectBean']]
    """

    kwargs = _get_kwargs(
        client=client,
        compute_metrics=compute_metrics,
        compute_owners=compute_owners,
        compute_engines=compute_engines,
        estimated_counts=estimated_counts,
        group_name=group_name,
        username=username,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
    compute_owners: Union[Unset, None, bool] = False,
    compute_engines: Union[Unset, None, bool] = False,
    estimated_counts: Union[Unset, None, bool] = False,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Optional[List["ProjectBean"]]:
    """Get projects

    Args:
        compute_metrics (Union[Unset, None, bool]):
        compute_owners (Union[Unset, None, bool]):
        compute_engines (Union[Unset, None, bool]):
        estimated_counts (Union[Unset, None, bool]):
        group_name (Union[Unset, None, str]):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ProjectBean']]
    """

    return (
        await asyncio_detailed(
            client=client,
            compute_metrics=compute_metrics,
            compute_owners=compute_owners,
            compute_engines=compute_engines,
            estimated_counts=estimated_counts,
            group_name=group_name,
            username=username,
        )
    ).parsed

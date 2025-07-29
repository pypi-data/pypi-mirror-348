from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.project_bean import ProjectBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    compute_metrics: Union[Unset, bool] = False,
    compute_owners: Union[Unset, bool] = False,
    compute_engines: Union[Unset, bool] = False,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["computeMetrics"] = compute_metrics

    params["computeOwners"] = compute_owners

    params["computeEngines"] = compute_engines

    params["groupName"] = group_name

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["ProjectBean"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_project_bean_array_item_data in _response_200:
            componentsschemas_project_bean_array_item = ProjectBean.from_dict(
                componentsschemas_project_bean_array_item_data
            )

            response_200.append(componentsschemas_project_bean_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ProjectBean"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
    compute_owners: Union[Unset, bool] = False,
    compute_engines: Union[Unset, bool] = False,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["ProjectBean"]]:
    """Get projects

    Args:
        compute_metrics (Union[Unset, bool]):  Default: False.
        compute_owners (Union[Unset, bool]):  Default: False.
        compute_engines (Union[Unset, bool]):  Default: False.
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ProjectBean']]
    """

    kwargs = _get_kwargs(
        compute_metrics=compute_metrics,
        compute_owners=compute_owners,
        compute_engines=compute_engines,
        group_name=group_name,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
    compute_owners: Union[Unset, bool] = False,
    compute_engines: Union[Unset, bool] = False,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Optional[list["ProjectBean"]]:
    """Get projects

    Args:
        compute_metrics (Union[Unset, bool]):  Default: False.
        compute_owners (Union[Unset, bool]):  Default: False.
        compute_engines (Union[Unset, bool]):  Default: False.
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ProjectBean']
    """

    return sync_detailed(
        client=client,
        compute_metrics=compute_metrics,
        compute_owners=compute_owners,
        compute_engines=compute_engines,
        group_name=group_name,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
    compute_owners: Union[Unset, bool] = False,
    compute_engines: Union[Unset, bool] = False,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["ProjectBean"]]:
    """Get projects

    Args:
        compute_metrics (Union[Unset, bool]):  Default: False.
        compute_owners (Union[Unset, bool]):  Default: False.
        compute_engines (Union[Unset, bool]):  Default: False.
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ProjectBean']]
    """

    kwargs = _get_kwargs(
        compute_metrics=compute_metrics,
        compute_owners=compute_owners,
        compute_engines=compute_engines,
        group_name=group_name,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
    compute_owners: Union[Unset, bool] = False,
    compute_engines: Union[Unset, bool] = False,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Optional[list["ProjectBean"]]:
    """Get projects

    Args:
        compute_metrics (Union[Unset, bool]):  Default: False.
        compute_owners (Union[Unset, bool]):  Default: False.
        compute_engines (Union[Unset, bool]):  Default: False.
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ProjectBean']
    """

    return (
        await asyncio_detailed(
            client=client,
            compute_metrics=compute_metrics,
            compute_owners=compute_owners,
            compute_engines=compute_engines,
            group_name=group_name,
            username=username,
        )
    ).parsed

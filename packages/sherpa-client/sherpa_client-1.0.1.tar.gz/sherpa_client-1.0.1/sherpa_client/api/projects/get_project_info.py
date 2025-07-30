from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.project_bean import ProjectBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    compute_metrics: Union[Unset, bool] = False,
    compute_owner: Union[Unset, bool] = True,
    compute_engines: Union[Unset, bool] = True,
    estimated_counts: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["computeMetrics"] = compute_metrics

    params["computeOwner"] = compute_owner

    params["computeEngines"] = compute_engines

    params["estimatedCounts"] = estimated_counts

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_name}/_info".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ProjectBean]:
    if response.status_code == 200:
        response_200 = ProjectBean.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ProjectBean]:
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
    compute_metrics: Union[Unset, bool] = False,
    compute_owner: Union[Unset, bool] = True,
    compute_engines: Union[Unset, bool] = True,
    estimated_counts: Union[Unset, bool] = False,
) -> Response[ProjectBean]:
    """Get project information

    Args:
        project_name (str):
        compute_metrics (Union[Unset, bool]):  Default: False.
        compute_owner (Union[Unset, bool]):  Default: True.
        compute_engines (Union[Unset, bool]):  Default: True.
        estimated_counts (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        compute_metrics=compute_metrics,
        compute_owner=compute_owner,
        compute_engines=compute_engines,
        estimated_counts=estimated_counts,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
    compute_owner: Union[Unset, bool] = True,
    compute_engines: Union[Unset, bool] = True,
    estimated_counts: Union[Unset, bool] = False,
) -> Optional[ProjectBean]:
    """Get project information

    Args:
        project_name (str):
        compute_metrics (Union[Unset, bool]):  Default: False.
        compute_owner (Union[Unset, bool]):  Default: True.
        compute_engines (Union[Unset, bool]):  Default: True.
        estimated_counts (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProjectBean
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        compute_metrics=compute_metrics,
        compute_owner=compute_owner,
        compute_engines=compute_engines,
        estimated_counts=estimated_counts,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
    compute_owner: Union[Unset, bool] = True,
    compute_engines: Union[Unset, bool] = True,
    estimated_counts: Union[Unset, bool] = False,
) -> Response[ProjectBean]:
    """Get project information

    Args:
        project_name (str):
        compute_metrics (Union[Unset, bool]):  Default: False.
        compute_owner (Union[Unset, bool]):  Default: True.
        compute_engines (Union[Unset, bool]):  Default: True.
        estimated_counts (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        compute_metrics=compute_metrics,
        compute_owner=compute_owner,
        compute_engines=compute_engines,
        estimated_counts=estimated_counts,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
    compute_owner: Union[Unset, bool] = True,
    compute_engines: Union[Unset, bool] = True,
    estimated_counts: Union[Unset, bool] = False,
) -> Optional[ProjectBean]:
    """Get project information

    Args:
        project_name (str):
        compute_metrics (Union[Unset, bool]):  Default: False.
        compute_owner (Union[Unset, bool]):  Default: True.
        compute_engines (Union[Unset, bool]):  Default: True.
        estimated_counts (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProjectBean
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            compute_metrics=compute_metrics,
            compute_owner=compute_owner,
            compute_engines=compute_engines,
            estimated_counts=estimated_counts,
        )
    ).parsed

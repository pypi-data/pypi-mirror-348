from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.project_bean import ProjectBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
    compute_owner: Union[Unset, None, bool] = True,
    compute_engines: Union[Unset, None, bool] = True,
    estimated_counts: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/_info".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["computeMetrics"] = compute_metrics

    params["computeOwner"] = compute_owner

    params["computeEngines"] = compute_engines

    params["estimatedCounts"] = estimated_counts

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[ProjectBean]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ProjectBean.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ProjectBean]:
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
    compute_metrics: Union[Unset, None, bool] = False,
    compute_owner: Union[Unset, None, bool] = True,
    compute_engines: Union[Unset, None, bool] = True,
    estimated_counts: Union[Unset, None, bool] = False,
) -> Response[ProjectBean]:
    """Get project information

    Args:
        project_name (str):
        compute_metrics (Union[Unset, None, bool]):
        compute_owner (Union[Unset, None, bool]):  Default: True.
        compute_engines (Union[Unset, None, bool]):  Default: True.
        estimated_counts (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        compute_metrics=compute_metrics,
        compute_owner=compute_owner,
        compute_engines=compute_engines,
        estimated_counts=estimated_counts,
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
    compute_metrics: Union[Unset, None, bool] = False,
    compute_owner: Union[Unset, None, bool] = True,
    compute_engines: Union[Unset, None, bool] = True,
    estimated_counts: Union[Unset, None, bool] = False,
) -> Optional[ProjectBean]:
    """Get project information

    Args:
        project_name (str):
        compute_metrics (Union[Unset, None, bool]):
        compute_owner (Union[Unset, None, bool]):  Default: True.
        compute_engines (Union[Unset, None, bool]):  Default: True.
        estimated_counts (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectBean]
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
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
    compute_owner: Union[Unset, None, bool] = True,
    compute_engines: Union[Unset, None, bool] = True,
    estimated_counts: Union[Unset, None, bool] = False,
) -> Response[ProjectBean]:
    """Get project information

    Args:
        project_name (str):
        compute_metrics (Union[Unset, None, bool]):
        compute_owner (Union[Unset, None, bool]):  Default: True.
        compute_engines (Union[Unset, None, bool]):  Default: True.
        estimated_counts (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        compute_metrics=compute_metrics,
        compute_owner=compute_owner,
        compute_engines=compute_engines,
        estimated_counts=estimated_counts,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    compute_metrics: Union[Unset, None, bool] = False,
    compute_owner: Union[Unset, None, bool] = True,
    compute_engines: Union[Unset, None, bool] = True,
    estimated_counts: Union[Unset, None, bool] = False,
) -> Optional[ProjectBean]:
    """Get project information

    Args:
        project_name (str):
        compute_metrics (Union[Unset, None, bool]):
        compute_owner (Union[Unset, None, bool]):  Default: True.
        compute_engines (Union[Unset, None, bool]):  Default: True.
        estimated_counts (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectBean]
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

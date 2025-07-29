from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.plan_operation_response import PlanOperationResponse
from ...models.plan_patch import PlanPatch
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    name: str,
    *,
    body: PlanPatch,
    dry_run: Union[Unset, bool] = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["dryRun"] = dry_run

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/projects/{project_name}/plans/{name}".format(
            project_name=project_name,
            name=name,
        ),
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/merge-patch+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PlanOperationResponse]]:
    if response.status_code == 200:
        response_200 = PlanOperationResponse.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, PlanOperationResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: PlanPatch,
    dry_run: Union[Unset, bool] = False,
) -> Response[Union[Any, PlanOperationResponse]]:
    """Partially update a plan

    Args:
        project_name (str):
        name (str):
        dry_run (Union[Unset, bool]):  Default: False.
        body (PlanPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PlanOperationResponse]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        name=name,
        body=body,
        dry_run=dry_run,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: PlanPatch,
    dry_run: Union[Unset, bool] = False,
) -> Optional[Union[Any, PlanOperationResponse]]:
    """Partially update a plan

    Args:
        project_name (str):
        name (str):
        dry_run (Union[Unset, bool]):  Default: False.
        body (PlanPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PlanOperationResponse]
    """

    return sync_detailed(
        project_name=project_name,
        name=name,
        client=client,
        body=body,
        dry_run=dry_run,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: PlanPatch,
    dry_run: Union[Unset, bool] = False,
) -> Response[Union[Any, PlanOperationResponse]]:
    """Partially update a plan

    Args:
        project_name (str):
        name (str):
        dry_run (Union[Unset, bool]):  Default: False.
        body (PlanPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PlanOperationResponse]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        name=name,
        body=body,
        dry_run=dry_run,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: PlanPatch,
    dry_run: Union[Unset, bool] = False,
) -> Optional[Union[Any, PlanOperationResponse]]:
    """Partially update a plan

    Args:
        project_name (str):
        name (str):
        dry_run (Union[Unset, bool]):  Default: False.
        body (PlanPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PlanOperationResponse]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            name=name,
            client=client,
            body=body,
            dry_run=dry_run,
        )
    ).parsed

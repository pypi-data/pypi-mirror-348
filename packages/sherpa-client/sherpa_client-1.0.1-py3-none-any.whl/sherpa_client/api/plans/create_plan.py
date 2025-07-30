from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.new_named_annotation_plan import NewNamedAnnotationPlan
from ...models.plan_operation_response import PlanOperationResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    body: NewNamedAnnotationPlan,
    dry_run: Union[Unset, bool] = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["dryRun"] = dry_run

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/plans".format(
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
) -> Optional[PlanOperationResponse]:
    if response.status_code == 200:
        response_200 = PlanOperationResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PlanOperationResponse]:
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
    body: NewNamedAnnotationPlan,
    dry_run: Union[Unset, bool] = False,
) -> Response[PlanOperationResponse]:
    """Create a plan

    Args:
        project_name (str):
        dry_run (Union[Unset, bool]):  Default: False.
        body (NewNamedAnnotationPlan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlanOperationResponse]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        body=body,
        dry_run=dry_run,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewNamedAnnotationPlan,
    dry_run: Union[Unset, bool] = False,
) -> Optional[PlanOperationResponse]:
    """Create a plan

    Args:
        project_name (str):
        dry_run (Union[Unset, bool]):  Default: False.
        body (NewNamedAnnotationPlan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PlanOperationResponse
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        body=body,
        dry_run=dry_run,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewNamedAnnotationPlan,
    dry_run: Union[Unset, bool] = False,
) -> Response[PlanOperationResponse]:
    """Create a plan

    Args:
        project_name (str):
        dry_run (Union[Unset, bool]):  Default: False.
        body (NewNamedAnnotationPlan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlanOperationResponse]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        body=body,
        dry_run=dry_run,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewNamedAnnotationPlan,
    dry_run: Union[Unset, bool] = False,
) -> Optional[PlanOperationResponse]:
    """Create a plan

    Args:
        project_name (str):
        dry_run (Union[Unset, bool]):  Default: False.
        body (NewNamedAnnotationPlan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PlanOperationResponse
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            body=body,
            dry_run=dry_run,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.new_named_annotation_plan import NewNamedAnnotationPlan
from ...models.plan_operation_response import PlanOperationResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    json_body: NewNamedAnnotationPlan,
    dry_run: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/plans".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["dryRun"] = dry_run

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[PlanOperationResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PlanOperationResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[PlanOperationResponse]:
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
    json_body: NewNamedAnnotationPlan,
    dry_run: Union[Unset, None, bool] = False,
) -> Response[PlanOperationResponse]:
    """Create a plan

    Args:
        project_name (str):
        dry_run (Union[Unset, None, bool]):
        json_body (NewNamedAnnotationPlan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlanOperationResponse]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        json_body=json_body,
        dry_run=dry_run,
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
    json_body: NewNamedAnnotationPlan,
    dry_run: Union[Unset, None, bool] = False,
) -> Optional[PlanOperationResponse]:
    """Create a plan

    Args:
        project_name (str):
        dry_run (Union[Unset, None, bool]):
        json_body (NewNamedAnnotationPlan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlanOperationResponse]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        json_body=json_body,
        dry_run=dry_run,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    json_body: NewNamedAnnotationPlan,
    dry_run: Union[Unset, None, bool] = False,
) -> Response[PlanOperationResponse]:
    """Create a plan

    Args:
        project_name (str):
        dry_run (Union[Unset, None, bool]):
        json_body (NewNamedAnnotationPlan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlanOperationResponse]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        json_body=json_body,
        dry_run=dry_run,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    json_body: NewNamedAnnotationPlan,
    dry_run: Union[Unset, None, bool] = False,
) -> Optional[PlanOperationResponse]:
    """Create a plan

    Args:
        project_name (str):
        dry_run (Union[Unset, None, bool]):
        json_body (NewNamedAnnotationPlan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlanOperationResponse]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            json_body=json_body,
            dry_run=dry_run,
        )
    ).parsed

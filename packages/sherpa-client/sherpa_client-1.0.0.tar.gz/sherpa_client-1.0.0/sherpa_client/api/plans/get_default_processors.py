from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.default_annotation_plan import DefaultAnnotationPlan
from ...models.default_processor_context import DefaultProcessorContext
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: DefaultProcessorContext,
    as_pipeline: Union[Unset, bool] = True,
    tags: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["asPipeline"] = as_pipeline

    params["tags"] = tags

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/processors/_default",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["DefaultAnnotationPlan"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_default_annotation_plan_array_item_data in _response_200:
            componentsschemas_default_annotation_plan_array_item = (
                DefaultAnnotationPlan.from_dict(
                    componentsschemas_default_annotation_plan_array_item_data
                )
            )

            response_200.append(componentsschemas_default_annotation_plan_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["DefaultAnnotationPlan"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: DefaultProcessorContext,
    as_pipeline: Union[Unset, bool] = True,
    tags: Union[Unset, str] = UNSET,
) -> Response[list["DefaultAnnotationPlan"]]:
    """Get default processors given a project configuration

    Args:
        as_pipeline (Union[Unset, bool]):  Default: True.
        tags (Union[Unset, str]):
        body (DefaultProcessorContext):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['DefaultAnnotationPlan']]
    """

    kwargs = _get_kwargs(
        body=body,
        as_pipeline=as_pipeline,
        tags=tags,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: DefaultProcessorContext,
    as_pipeline: Union[Unset, bool] = True,
    tags: Union[Unset, str] = UNSET,
) -> Optional[list["DefaultAnnotationPlan"]]:
    """Get default processors given a project configuration

    Args:
        as_pipeline (Union[Unset, bool]):  Default: True.
        tags (Union[Unset, str]):
        body (DefaultProcessorContext):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['DefaultAnnotationPlan']
    """

    return sync_detailed(
        client=client,
        body=body,
        as_pipeline=as_pipeline,
        tags=tags,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: DefaultProcessorContext,
    as_pipeline: Union[Unset, bool] = True,
    tags: Union[Unset, str] = UNSET,
) -> Response[list["DefaultAnnotationPlan"]]:
    """Get default processors given a project configuration

    Args:
        as_pipeline (Union[Unset, bool]):  Default: True.
        tags (Union[Unset, str]):
        body (DefaultProcessorContext):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['DefaultAnnotationPlan']]
    """

    kwargs = _get_kwargs(
        body=body,
        as_pipeline=as_pipeline,
        tags=tags,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: DefaultProcessorContext,
    as_pipeline: Union[Unset, bool] = True,
    tags: Union[Unset, str] = UNSET,
) -> Optional[list["DefaultAnnotationPlan"]]:
    """Get default processors given a project configuration

    Args:
        as_pipeline (Union[Unset, bool]):  Default: True.
        tags (Union[Unset, str]):
        body (DefaultProcessorContext):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['DefaultAnnotationPlan']
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            as_pipeline=as_pipeline,
            tags=tags,
        )
    ).parsed

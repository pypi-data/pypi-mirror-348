from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.annotation_metrics import AnnotationMetrics
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    facet: Union[Unset, str] = "",
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["facet"] = facet

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_name}/annotationMetrics".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AnnotationMetrics]:
    if response.status_code == 200:
        response_200 = AnnotationMetrics.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AnnotationMetrics]:
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
    facet: Union[Unset, str] = "",
) -> Response[AnnotationMetrics]:
    """Get some metrics on annotations

    Args:
        project_name (str):
        facet (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotationMetrics]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        facet=facet,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    facet: Union[Unset, str] = "",
) -> Optional[AnnotationMetrics]:
    """Get some metrics on annotations

    Args:
        project_name (str):
        facet (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnnotationMetrics
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        facet=facet,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    facet: Union[Unset, str] = "",
) -> Response[AnnotationMetrics]:
    """Get some metrics on annotations

    Args:
        project_name (str):
        facet (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotationMetrics]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        facet=facet,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    facet: Union[Unset, str] = "",
) -> Optional[AnnotationMetrics]:
    """Get some metrics on annotations

    Args:
        project_name (str):
        facet (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnnotationMetrics
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            facet=facet,
        )
    ).parsed

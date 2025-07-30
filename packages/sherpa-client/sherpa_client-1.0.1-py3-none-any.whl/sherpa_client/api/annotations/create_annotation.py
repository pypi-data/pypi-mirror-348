from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.annotation import Annotation
from ...models.annotation_id import AnnotationId
from ...types import Response


def _get_kwargs(
    project_name: str,
    *,
    body: Annotation,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/annotations".format(
            project_name=project_name,
        ),
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AnnotationId]:
    if response.status_code == 200:
        response_200 = AnnotationId.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AnnotationId]:
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
    body: Annotation,
) -> Response[AnnotationId]:
    """Add an annotation into the dataset

    Args:
        project_name (str):
        body (Annotation): A document annotation

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotationId]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Annotation,
) -> Optional[AnnotationId]:
    """Add an annotation into the dataset

    Args:
        project_name (str):
        body (Annotation): A document annotation

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnnotationId
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Annotation,
) -> Response[AnnotationId]:
    """Add an annotation into the dataset

    Args:
        project_name (str):
        body (Annotation): A document annotation

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotationId]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Annotation,
) -> Optional[AnnotationId]:
    """Add an annotation into the dataset

    Args:
        project_name (str):
        body (Annotation): A document annotation

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnnotationId
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            body=body,
        )
    ).parsed

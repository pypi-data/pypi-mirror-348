from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.label_set import LabelSet
from ...models.label_set_update import LabelSetUpdate
from ...types import Response


def _get_kwargs(
    project_name: str,
    name: str,
    *,
    body: LabelSetUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/projects/{project_name}/label_sets/{name}".format(
            project_name=project_name,
            name=name,
        ),
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, LabelSet]]:
    if response.status_code == 200:
        response_200 = LabelSet.from_dict(response.json())

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
) -> Response[Union[Any, LabelSet]]:
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
    body: LabelSetUpdate,
) -> Response[Union[Any, LabelSet]]:
    """Update a labelSet

    Args:
        project_name (str):
        name (str):
        body (LabelSetUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LabelSet]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        name=name,
        body=body,
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
    body: LabelSetUpdate,
) -> Optional[Union[Any, LabelSet]]:
    """Update a labelSet

    Args:
        project_name (str):
        name (str):
        body (LabelSetUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LabelSet]
    """

    return sync_detailed(
        project_name=project_name,
        name=name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: LabelSetUpdate,
) -> Response[Union[Any, LabelSet]]:
    """Update a labelSet

    Args:
        project_name (str):
        name (str):
        body (LabelSetUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LabelSet]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        name=name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: LabelSetUpdate,
) -> Optional[Union[Any, LabelSet]]:
    """Update a labelSet

    Args:
        project_name (str):
        name (str):
        body (LabelSetUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LabelSet]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            name=name,
            client=client,
            body=body,
        )
    ).parsed

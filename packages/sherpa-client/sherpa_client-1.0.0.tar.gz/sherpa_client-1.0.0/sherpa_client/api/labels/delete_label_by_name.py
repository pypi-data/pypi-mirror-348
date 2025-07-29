from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_response import DeleteResponse
from ...types import Response


def _get_kwargs(
    project_name: str,
    label_name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{project_name}/labels/{label_name}".format(
            project_name=project_name,
            label_name=label_name,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, DeleteResponse]]:
    if response.status_code == 200:
        response_200 = DeleteResponse.from_dict(response.json())

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
) -> Response[Union[Any, DeleteResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    label_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, DeleteResponse]]:
    """Remove label by name

    Args:
        project_name (str):
        label_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteResponse]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        label_name=label_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    label_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, DeleteResponse]]:
    """Remove label by name

    Args:
        project_name (str):
        label_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteResponse]
    """

    return sync_detailed(
        project_name=project_name,
        label_name=label_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    label_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, DeleteResponse]]:
    """Remove label by name

    Args:
        project_name (str):
        label_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteResponse]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        label_name=label_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    label_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, DeleteResponse]]:
    """Remove label by name

    Args:
        project_name (str):
        label_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteResponse]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            label_name=label_name,
            client=client,
        )
    ).parsed

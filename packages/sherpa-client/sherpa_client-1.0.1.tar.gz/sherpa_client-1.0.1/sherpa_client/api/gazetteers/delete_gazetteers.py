from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_response import DeleteResponse
from ...types import UNSET, Response


def _get_kwargs(
    project_name: str,
    *,
    names: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["names"] = names

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{project_name}/gazetteers".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[DeleteResponse]:
    if response.status_code == 200:
        response_200 = DeleteResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DeleteResponse]:
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
    names: str,
) -> Response[DeleteResponse]:
    """Delete gazetteers

    Args:
        project_name (str):
        names (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteResponse]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        names=names,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    names: str,
) -> Optional[DeleteResponse]:
    """Delete gazetteers

    Args:
        project_name (str):
        names (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteResponse
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        names=names,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    names: str,
) -> Response[DeleteResponse]:
    """Delete gazetteers

    Args:
        project_name (str):
        names (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteResponse]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        names=names,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    names: str,
) -> Optional[DeleteResponse]:
    """Delete gazetteers

    Args:
        project_name (str):
        names (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteResponse
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            names=names,
        )
    ).parsed

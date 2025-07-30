from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.created_by_count import CreatedByCount
from ...types import Response


def _get_kwargs(
    project_name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/categories/_count_creators".format(
            project_name=project_name,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["CreatedByCount"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_created_by_count_array_item_data in _response_200:
            componentsschemas_created_by_count_array_item = CreatedByCount.from_dict(
                componentsschemas_created_by_count_array_item_data
            )

            response_200.append(componentsschemas_created_by_count_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["CreatedByCount"]]:
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
) -> Response[list["CreatedByCount"]]:
    """Get categories count per creators

    Args:
        project_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CreatedByCount']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[list["CreatedByCount"]]:
    """Get categories count per creators

    Args:
        project_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CreatedByCount']
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[list["CreatedByCount"]]:
    """Get categories count per creators

    Args:
        project_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CreatedByCount']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[list["CreatedByCount"]]:
    """Get categories count per creators

    Args:
        project_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CreatedByCount']
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
        )
    ).parsed

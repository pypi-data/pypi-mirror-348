from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.label import Label
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    label_name: str,
    *,
    include_count: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["includeCount"] = include_count

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_name}/label/{label_name}".format(
            project_name=project_name,
            label_name=label_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Label]:
    if response.status_code == 200:
        response_200 = Label.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Label]:
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
    include_count: Union[Unset, bool] = False,
) -> Response[Label]:
    """Get label

    Args:
        project_name (str):
        label_name (str):
        include_count (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Label]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        label_name=label_name,
        include_count=include_count,
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
    include_count: Union[Unset, bool] = False,
) -> Optional[Label]:
    """Get label

    Args:
        project_name (str):
        label_name (str):
        include_count (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Label
    """

    return sync_detailed(
        project_name=project_name,
        label_name=label_name,
        client=client,
        include_count=include_count,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    label_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_count: Union[Unset, bool] = False,
) -> Response[Label]:
    """Get label

    Args:
        project_name (str):
        label_name (str):
        include_count (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Label]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        label_name=label_name,
        include_count=include_count,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    label_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_count: Union[Unset, bool] = False,
) -> Optional[Label]:
    """Get label

    Args:
        project_name (str):
        label_name (str):
        include_count (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Label
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            label_name=label_name,
            client=client,
            include_count=include_count,
        )
    ).parsed

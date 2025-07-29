from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_theme_config_schema_response_200 import (
    GetThemeConfigSchemaResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    ui_schema: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["uiSchema"] = ui_schema

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/themes/_schema",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetThemeConfigSchemaResponse200]:
    if response.status_code == 200:
        response_200 = GetThemeConfigSchemaResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetThemeConfigSchemaResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    ui_schema: Union[Unset, bool] = False,
) -> Response[GetThemeConfigSchemaResponse200]:
    """Get the schema of a UI theme configuration

    Args:
        ui_schema (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetThemeConfigSchemaResponse200]
    """

    kwargs = _get_kwargs(
        ui_schema=ui_schema,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    ui_schema: Union[Unset, bool] = False,
) -> Optional[GetThemeConfigSchemaResponse200]:
    """Get the schema of a UI theme configuration

    Args:
        ui_schema (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetThemeConfigSchemaResponse200
    """

    return sync_detailed(
        client=client,
        ui_schema=ui_schema,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    ui_schema: Union[Unset, bool] = False,
) -> Response[GetThemeConfigSchemaResponse200]:
    """Get the schema of a UI theme configuration

    Args:
        ui_schema (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetThemeConfigSchemaResponse200]
    """

    kwargs = _get_kwargs(
        ui_schema=ui_schema,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    ui_schema: Union[Unset, bool] = False,
) -> Optional[GetThemeConfigSchemaResponse200]:
    """Get the schema of a UI theme configuration

    Args:
        ui_schema (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetThemeConfigSchemaResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            ui_schema=ui_schema,
        )
    ).parsed

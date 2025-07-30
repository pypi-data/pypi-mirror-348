from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.get_theme_config_schema_response_200 import GetThemeConfigSchemaResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    ui_schema: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/themes/_schema".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["uiSchema"] = ui_schema

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[GetThemeConfigSchemaResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetThemeConfigSchemaResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[GetThemeConfigSchemaResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    ui_schema: Union[Unset, None, bool] = False,
) -> Response[GetThemeConfigSchemaResponse200]:
    """Get the schema of a UI theme configuration

    Args:
        ui_schema (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetThemeConfigSchemaResponse200]
    """

    kwargs = _get_kwargs(
        client=client,
        ui_schema=ui_schema,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    ui_schema: Union[Unset, None, bool] = False,
) -> Optional[GetThemeConfigSchemaResponse200]:
    """Get the schema of a UI theme configuration

    Args:
        ui_schema (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetThemeConfigSchemaResponse200]
    """

    return sync_detailed(
        client=client,
        ui_schema=ui_schema,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    ui_schema: Union[Unset, None, bool] = False,
) -> Response[GetThemeConfigSchemaResponse200]:
    """Get the schema of a UI theme configuration

    Args:
        ui_schema (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetThemeConfigSchemaResponse200]
    """

    kwargs = _get_kwargs(
        client=client,
        ui_schema=ui_schema,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    ui_schema: Union[Unset, None, bool] = False,
) -> Optional[GetThemeConfigSchemaResponse200]:
    """Get the schema of a UI theme configuration

    Args:
        ui_schema (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetThemeConfigSchemaResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            ui_schema=ui_schema,
        )
    ).parsed

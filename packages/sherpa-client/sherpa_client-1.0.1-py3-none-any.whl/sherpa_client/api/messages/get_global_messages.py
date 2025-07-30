from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_global_messages_scopes_item import GetGlobalMessagesScopesItem
from ...models.message import Message
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    group: Union[Unset, str] = UNSET,
    language: Union[Unset, str] = UNSET,
    read: Union[Unset, bool] = UNSET,
    scopes: Union[Unset, list[GetGlobalMessagesScopesItem]] = UNSET,
    output_fields: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["group"] = group

    params["language"] = language

    params["read"] = read

    json_scopes: Union[Unset, list[str]] = UNSET
    if not isinstance(scopes, Unset):
        json_scopes = []
        for scopes_item_data in scopes:
            scopes_item = scopes_item_data.value
            json_scopes.append(scopes_item)

    params["scopes"] = json_scopes

    params["outputFields"] = output_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/messages",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["Message"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_message_array_item_data in _response_200:
            componentsschemas_message_array_item = Message.from_dict(
                componentsschemas_message_array_item_data
            )

            response_200.append(componentsschemas_message_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Message"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    group: Union[Unset, str] = UNSET,
    language: Union[Unset, str] = UNSET,
    read: Union[Unset, bool] = UNSET,
    scopes: Union[Unset, list[GetGlobalMessagesScopesItem]] = UNSET,
    output_fields: Union[Unset, str] = UNSET,
) -> Response[list["Message"]]:
    """Get messages of current user

    Args:
        group (Union[Unset, str]):
        language (Union[Unset, str]):
        read (Union[Unset, bool]):
        scopes (Union[Unset, list[GetGlobalMessagesScopesItem]]):
        output_fields (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Message']]
    """

    kwargs = _get_kwargs(
        group=group,
        language=language,
        read=read,
        scopes=scopes,
        output_fields=output_fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    group: Union[Unset, str] = UNSET,
    language: Union[Unset, str] = UNSET,
    read: Union[Unset, bool] = UNSET,
    scopes: Union[Unset, list[GetGlobalMessagesScopesItem]] = UNSET,
    output_fields: Union[Unset, str] = UNSET,
) -> Optional[list["Message"]]:
    """Get messages of current user

    Args:
        group (Union[Unset, str]):
        language (Union[Unset, str]):
        read (Union[Unset, bool]):
        scopes (Union[Unset, list[GetGlobalMessagesScopesItem]]):
        output_fields (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Message']
    """

    return sync_detailed(
        client=client,
        group=group,
        language=language,
        read=read,
        scopes=scopes,
        output_fields=output_fields,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    group: Union[Unset, str] = UNSET,
    language: Union[Unset, str] = UNSET,
    read: Union[Unset, bool] = UNSET,
    scopes: Union[Unset, list[GetGlobalMessagesScopesItem]] = UNSET,
    output_fields: Union[Unset, str] = UNSET,
) -> Response[list["Message"]]:
    """Get messages of current user

    Args:
        group (Union[Unset, str]):
        language (Union[Unset, str]):
        read (Union[Unset, bool]):
        scopes (Union[Unset, list[GetGlobalMessagesScopesItem]]):
        output_fields (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Message']]
    """

    kwargs = _get_kwargs(
        group=group,
        language=language,
        read=read,
        scopes=scopes,
        output_fields=output_fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    group: Union[Unset, str] = UNSET,
    language: Union[Unset, str] = UNSET,
    read: Union[Unset, bool] = UNSET,
    scopes: Union[Unset, list[GetGlobalMessagesScopesItem]] = UNSET,
    output_fields: Union[Unset, str] = UNSET,
) -> Optional[list["Message"]]:
    """Get messages of current user

    Args:
        group (Union[Unset, str]):
        language (Union[Unset, str]):
        read (Union[Unset, bool]):
        scopes (Union[Unset, list[GetGlobalMessagesScopesItem]]):
        output_fields (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Message']
    """

    return (
        await asyncio_detailed(
            client=client,
            group=group,
            language=language,
            read=read,
            scopes=scopes,
            output_fields=output_fields,
        )
    ).parsed

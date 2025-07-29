from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_many_response import DeleteManyResponse
from ...models.item_ref import ItemRef
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    body: list["ItemRef"],
    all_: Union[Unset, bool] = False,
    with_details: Union[Unset, bool] = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["all"] = all_

    params["withDetails"] = with_details

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/alt_texts/_delete".format(
            project_name=project_name,
        ),
        "params": params,
    }

    _body = []
    for componentsschemas_item_ref_array_item_data in body:
        componentsschemas_item_ref_array_item = (
            componentsschemas_item_ref_array_item_data.to_dict()
        )
        _body.append(componentsschemas_item_ref_array_item)

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[DeleteManyResponse]:
    if response.status_code == 200:
        response_200 = DeleteManyResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DeleteManyResponse]:
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
    body: list["ItemRef"],
    all_: Union[Unset, bool] = False,
    with_details: Union[Unset, bool] = False,
) -> Response[DeleteManyResponse]:
    """Remove some or all alternative document texts

    Args:
        project_name (str):
        all_ (Union[Unset, bool]):  Default: False.
        with_details (Union[Unset, bool]):  Default: False.
        body (list['ItemRef']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteManyResponse]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        body=body,
        all_=all_,
        with_details=with_details,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["ItemRef"],
    all_: Union[Unset, bool] = False,
    with_details: Union[Unset, bool] = False,
) -> Optional[DeleteManyResponse]:
    """Remove some or all alternative document texts

    Args:
        project_name (str):
        all_ (Union[Unset, bool]):  Default: False.
        with_details (Union[Unset, bool]):  Default: False.
        body (list['ItemRef']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteManyResponse
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        body=body,
        all_=all_,
        with_details=with_details,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["ItemRef"],
    all_: Union[Unset, bool] = False,
    with_details: Union[Unset, bool] = False,
) -> Response[DeleteManyResponse]:
    """Remove some or all alternative document texts

    Args:
        project_name (str):
        all_ (Union[Unset, bool]):  Default: False.
        with_details (Union[Unset, bool]):  Default: False.
        body (list['ItemRef']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteManyResponse]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        body=body,
        all_=all_,
        with_details=with_details,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["ItemRef"],
    all_: Union[Unset, bool] = False,
    with_details: Union[Unset, bool] = False,
) -> Optional[DeleteManyResponse]:
    """Remove some or all alternative document texts

    Args:
        project_name (str):
        all_ (Union[Unset, bool]):  Default: False.
        with_details (Union[Unset, bool]):  Default: False.
        body (list['ItemRef']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteManyResponse
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            body=body,
            all_=all_,
            with_details=with_details,
        )
    ).parsed

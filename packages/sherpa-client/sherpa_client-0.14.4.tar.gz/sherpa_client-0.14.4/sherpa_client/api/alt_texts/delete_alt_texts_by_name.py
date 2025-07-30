from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.delete_many_response import DeleteManyResponse
from ...models.item_ref import ItemRef
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    json_body: List["ItemRef"],
    all_: Union[Unset, None, bool] = False,
    with_details: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/alt_texts/_delete".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["all"] = all_

    params["withDetails"] = with_details

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = []
    for componentsschemas_item_ref_array_item_data in json_body:
        componentsschemas_item_ref_array_item = componentsschemas_item_ref_array_item_data.to_dict()

        json_json_body.append(componentsschemas_item_ref_array_item)

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[DeleteManyResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteManyResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[DeleteManyResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    *,
    client: Client,
    json_body: List["ItemRef"],
    all_: Union[Unset, None, bool] = False,
    with_details: Union[Unset, None, bool] = False,
) -> Response[DeleteManyResponse]:
    """Remove some or all alternative document texts

    Args:
        project_name (str):
        all_ (Union[Unset, None, bool]):
        with_details (Union[Unset, None, bool]):
        json_body (List['ItemRef']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteManyResponse]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        json_body=json_body,
        all_=all_,
        with_details=with_details,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Client,
    json_body: List["ItemRef"],
    all_: Union[Unset, None, bool] = False,
    with_details: Union[Unset, None, bool] = False,
) -> Optional[DeleteManyResponse]:
    """Remove some or all alternative document texts

    Args:
        project_name (str):
        all_ (Union[Unset, None, bool]):
        with_details (Union[Unset, None, bool]):
        json_body (List['ItemRef']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteManyResponse]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        json_body=json_body,
        all_=all_,
        with_details=with_details,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    json_body: List["ItemRef"],
    all_: Union[Unset, None, bool] = False,
    with_details: Union[Unset, None, bool] = False,
) -> Response[DeleteManyResponse]:
    """Remove some or all alternative document texts

    Args:
        project_name (str):
        all_ (Union[Unset, None, bool]):
        with_details (Union[Unset, None, bool]):
        json_body (List['ItemRef']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteManyResponse]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        json_body=json_body,
        all_=all_,
        with_details=with_details,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    json_body: List["ItemRef"],
    all_: Union[Unset, None, bool] = False,
    with_details: Union[Unset, None, bool] = False,
) -> Optional[DeleteManyResponse]:
    """Remove some or all alternative document texts

    Args:
        project_name (str):
        all_ (Union[Unset, None, bool]):
        with_details (Union[Unset, None, bool]):
        json_body (List['ItemRef']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteManyResponse]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            json_body=json_body,
            all_=all_,
            with_details=with_details,
        )
    ).parsed

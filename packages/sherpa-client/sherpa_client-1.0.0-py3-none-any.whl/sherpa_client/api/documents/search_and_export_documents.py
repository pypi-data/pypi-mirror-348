from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document import Document
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    query: Union[Unset, str] = "",
    query_filter: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    output_fields: Union[Unset, str] = "",
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["query"] = query

    params["queryFilter"] = query_filter

    params["simpleQuery"] = simple_query

    json_selected_facets: Union[Unset, list[str]] = UNSET
    if not isinstance(selected_facets, Unset):
        json_selected_facets = selected_facets

    params["selectedFacets"] = json_selected_facets

    params["invertSearch"] = invert_search

    params["outputFields"] = output_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/documents/_search_and_export".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["Document"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_document_array_item_data in _response_200:
            componentsschemas_document_array_item = Document.from_dict(
                componentsschemas_document_array_item_data
            )

            response_200.append(componentsschemas_document_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Document"]]:
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
    query: Union[Unset, str] = "",
    query_filter: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    output_fields: Union[Unset, str] = "",
) -> Response[list["Document"]]:
    """Search for documents and export them

    Args:
        project_name (str):
        query (Union[Unset, str]):  Default: ''.
        query_filter (Union[Unset, str]):  Default: ''.
        simple_query (Union[Unset, bool]):  Default: False.
        selected_facets (Union[Unset, list[str]]):
        invert_search (Union[Unset, bool]):  Default: False.
        output_fields (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Document']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        query=query,
        query_filter=query_filter,
        simple_query=simple_query,
        selected_facets=selected_facets,
        invert_search=invert_search,
        output_fields=output_fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    query_filter: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    output_fields: Union[Unset, str] = "",
) -> Optional[list["Document"]]:
    """Search for documents and export them

    Args:
        project_name (str):
        query (Union[Unset, str]):  Default: ''.
        query_filter (Union[Unset, str]):  Default: ''.
        simple_query (Union[Unset, bool]):  Default: False.
        selected_facets (Union[Unset, list[str]]):
        invert_search (Union[Unset, bool]):  Default: False.
        output_fields (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Document']
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        query=query,
        query_filter=query_filter,
        simple_query=simple_query,
        selected_facets=selected_facets,
        invert_search=invert_search,
        output_fields=output_fields,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    query_filter: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    output_fields: Union[Unset, str] = "",
) -> Response[list["Document"]]:
    """Search for documents and export them

    Args:
        project_name (str):
        query (Union[Unset, str]):  Default: ''.
        query_filter (Union[Unset, str]):  Default: ''.
        simple_query (Union[Unset, bool]):  Default: False.
        selected_facets (Union[Unset, list[str]]):
        invert_search (Union[Unset, bool]):  Default: False.
        output_fields (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Document']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        query=query,
        query_filter=query_filter,
        simple_query=simple_query,
        selected_facets=selected_facets,
        invert_search=invert_search,
        output_fields=output_fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    query_filter: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    output_fields: Union[Unset, str] = "",
) -> Optional[list["Document"]]:
    """Search for documents and export them

    Args:
        project_name (str):
        query (Union[Unset, str]):  Default: ''.
        query_filter (Union[Unset, str]):  Default: ''.
        simple_query (Union[Unset, bool]):  Default: False.
        selected_facets (Union[Unset, list[str]]):
        invert_search (Union[Unset, bool]):  Default: False.
        output_fields (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Document']
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            query=query,
            query_filter=query_filter,
            simple_query=simple_query,
            selected_facets=selected_facets,
            invert_search=invert_search,
            output_fields=output_fields,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.label_set import LabelSet
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    include_labels: Union[Unset, bool] = True,
    include_labels_count: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["includeLabels"] = include_labels

    params["includeLabelsCount"] = include_labels_count

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_name}/label_sets".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["LabelSet"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_label_set_array_item_data in _response_200:
            componentsschemas_label_set_array_item = LabelSet.from_dict(
                componentsschemas_label_set_array_item_data
            )

            response_200.append(componentsschemas_label_set_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["LabelSet"]]:
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
    include_labels: Union[Unset, bool] = True,
    include_labels_count: Union[Unset, bool] = False,
) -> Response[list["LabelSet"]]:
    """Get list of labelSet

    Args:
        project_name (str):
        include_labels (Union[Unset, bool]):  Default: True.
        include_labels_count (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['LabelSet']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        include_labels=include_labels,
        include_labels_count=include_labels_count,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_labels: Union[Unset, bool] = True,
    include_labels_count: Union[Unset, bool] = False,
) -> Optional[list["LabelSet"]]:
    """Get list of labelSet

    Args:
        project_name (str):
        include_labels (Union[Unset, bool]):  Default: True.
        include_labels_count (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['LabelSet']
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        include_labels=include_labels,
        include_labels_count=include_labels_count,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_labels: Union[Unset, bool] = True,
    include_labels_count: Union[Unset, bool] = False,
) -> Response[list["LabelSet"]]:
    """Get list of labelSet

    Args:
        project_name (str):
        include_labels (Union[Unset, bool]):  Default: True.
        include_labels_count (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['LabelSet']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        include_labels=include_labels,
        include_labels_count=include_labels_count,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_labels: Union[Unset, bool] = True,
    include_labels_count: Union[Unset, bool] = False,
) -> Optional[list["LabelSet"]]:
    """Get list of labelSet

    Args:
        project_name (str):
        include_labels (Union[Unset, bool]):  Default: True.
        include_labels_count (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['LabelSet']
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            include_labels=include_labels,
            include_labels_count=include_labels_count,
        )
    ).parsed

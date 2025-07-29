from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.label_set import LabelSet
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    name: str,
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
        "url": "/projects/{project_name}/label_sets/{name}".format(
            project_name=project_name,
            name=name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, LabelSet]]:
    if response.status_code == 200:
        response_200 = LabelSet.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, LabelSet]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_labels: Union[Unset, bool] = True,
    include_labels_count: Union[Unset, bool] = False,
) -> Response[Union[Any, LabelSet]]:
    """Get a labelSet

    Args:
        project_name (str):
        name (str):
        include_labels (Union[Unset, bool]):  Default: True.
        include_labels_count (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LabelSet]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        name=name,
        include_labels=include_labels,
        include_labels_count=include_labels_count,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_labels: Union[Unset, bool] = True,
    include_labels_count: Union[Unset, bool] = False,
) -> Optional[Union[Any, LabelSet]]:
    """Get a labelSet

    Args:
        project_name (str):
        name (str):
        include_labels (Union[Unset, bool]):  Default: True.
        include_labels_count (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LabelSet]
    """

    return sync_detailed(
        project_name=project_name,
        name=name,
        client=client,
        include_labels=include_labels,
        include_labels_count=include_labels_count,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_labels: Union[Unset, bool] = True,
    include_labels_count: Union[Unset, bool] = False,
) -> Response[Union[Any, LabelSet]]:
    """Get a labelSet

    Args:
        project_name (str):
        name (str):
        include_labels (Union[Unset, bool]):  Default: True.
        include_labels_count (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LabelSet]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        name=name,
        include_labels=include_labels,
        include_labels_count=include_labels_count,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_labels: Union[Unset, bool] = True,
    include_labels_count: Union[Unset, bool] = False,
) -> Optional[Union[Any, LabelSet]]:
    """Get a labelSet

    Args:
        project_name (str):
        name (str):
        include_labels (Union[Unset, bool]):  Default: True.
        include_labels_count (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LabelSet]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            name=name,
            client=client,
            include_labels=include_labels,
            include_labels_count=include_labels_count,
        )
    ).parsed

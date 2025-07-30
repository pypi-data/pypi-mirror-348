from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.operation_count import OperationCount
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    labels: Union[Unset, list[str]] = UNSET,
    created_by: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_labels: Union[Unset, list[str]] = UNSET
    if not isinstance(labels, Unset):
        json_labels = labels

    params["labels"] = json_labels

    json_created_by: Union[Unset, list[str]] = UNSET
    if not isinstance(created_by, Unset):
        json_created_by = created_by

    params["createdBy"] = json_created_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/annotations/_clear".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[OperationCount]:
    if response.status_code == 200:
        response_200 = OperationCount.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OperationCount]:
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
    labels: Union[Unset, list[str]] = UNSET,
    created_by: Union[Unset, list[str]] = UNSET,
) -> Response[OperationCount]:
    """Delete annotations from the corpus

    Args:
        project_name (str):
        labels (Union[Unset, list[str]]):
        created_by (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OperationCount]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        labels=labels,
        created_by=created_by,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    labels: Union[Unset, list[str]] = UNSET,
    created_by: Union[Unset, list[str]] = UNSET,
) -> Optional[OperationCount]:
    """Delete annotations from the corpus

    Args:
        project_name (str):
        labels (Union[Unset, list[str]]):
        created_by (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OperationCount
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        labels=labels,
        created_by=created_by,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    labels: Union[Unset, list[str]] = UNSET,
    created_by: Union[Unset, list[str]] = UNSET,
) -> Response[OperationCount]:
    """Delete annotations from the corpus

    Args:
        project_name (str):
        labels (Union[Unset, list[str]]):
        created_by (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OperationCount]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        labels=labels,
        created_by=created_by,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    labels: Union[Unset, list[str]] = UNSET,
    created_by: Union[Unset, list[str]] = UNSET,
) -> Optional[OperationCount]:
    """Delete annotations from the corpus

    Args:
        project_name (str):
        labels (Union[Unset, list[str]]):
        created_by (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OperationCount
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            labels=labels,
            created_by=created_by,
        )
    ).parsed

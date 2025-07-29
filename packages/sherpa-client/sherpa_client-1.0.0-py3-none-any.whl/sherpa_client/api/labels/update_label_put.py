from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.label import Label
from ...models.label_update import LabelUpdate
from ...types import Response


def _get_kwargs(
    project_name: str,
    label_name: str,
    *,
    body: LabelUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{project_name}/labels/{label_name}".format(
            project_name=project_name,
            label_name=label_name,
        ),
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    body: LabelUpdate,
) -> Response[Label]:
    """Update a label (Please use PATCH instead of PUT)

    Args:
        project_name (str):
        label_name (str):
        body (LabelUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Label]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        label_name=label_name,
        body=body,
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
    body: LabelUpdate,
) -> Optional[Label]:
    """Update a label (Please use PATCH instead of PUT)

    Args:
        project_name (str):
        label_name (str):
        body (LabelUpdate):

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
        body=body,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    label_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: LabelUpdate,
) -> Response[Label]:
    """Update a label (Please use PATCH instead of PUT)

    Args:
        project_name (str):
        label_name (str):
        body (LabelUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Label]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        label_name=label_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    label_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: LabelUpdate,
) -> Optional[Label]:
    """Update a label (Please use PATCH instead of PUT)

    Args:
        project_name (str):
        label_name (str):
        body (LabelUpdate):

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
            body=body,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.lexicon import Lexicon
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    compute_metrics: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["computeMetrics"] = compute_metrics

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_name}/lexicons".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["Lexicon"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_lexicon_array_item_data in _response_200:
            componentsschemas_lexicon_array_item = Lexicon.from_dict(
                componentsschemas_lexicon_array_item_data
            )

            response_200.append(componentsschemas_lexicon_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Lexicon"]]:
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
    compute_metrics: Union[Unset, bool] = False,
) -> Response[list["Lexicon"]]:
    """Get lexicons

    Args:
        project_name (str):
        compute_metrics (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Lexicon']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        compute_metrics=compute_metrics,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
) -> Optional[list["Lexicon"]]:
    """Get lexicons

    Args:
        project_name (str):
        compute_metrics (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Lexicon']
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        compute_metrics=compute_metrics,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
) -> Response[list["Lexicon"]]:
    """Get lexicons

    Args:
        project_name (str):
        compute_metrics (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Lexicon']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        compute_metrics=compute_metrics,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
) -> Optional[list["Lexicon"]]:
    """Get lexicons

    Args:
        project_name (str):
        compute_metrics (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Lexicon']
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            compute_metrics=compute_metrics,
        )
    ).parsed

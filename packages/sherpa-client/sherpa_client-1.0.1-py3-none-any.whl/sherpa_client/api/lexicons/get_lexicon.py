from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.lexicon import Lexicon
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    lexicon_name: str,
    *,
    compute_metrics: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["computeMetrics"] = compute_metrics

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_name}/lexicons/{lexicon_name}".format(
            project_name=project_name,
            lexicon_name=lexicon_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Lexicon]]:
    if response.status_code == 200:
        response_200 = Lexicon.from_dict(response.json())

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
) -> Response[Union[Any, Lexicon]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    lexicon_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
) -> Response[Union[Any, Lexicon]]:
    """Get a lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        compute_metrics (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Lexicon]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        lexicon_name=lexicon_name,
        compute_metrics=compute_metrics,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    lexicon_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
) -> Optional[Union[Any, Lexicon]]:
    """Get a lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        compute_metrics (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Lexicon]
    """

    return sync_detailed(
        project_name=project_name,
        lexicon_name=lexicon_name,
        client=client,
        compute_metrics=compute_metrics,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    lexicon_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
) -> Response[Union[Any, Lexicon]]:
    """Get a lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        compute_metrics (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Lexicon]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        lexicon_name=lexicon_name,
        compute_metrics=compute_metrics,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    lexicon_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_metrics: Union[Unset, bool] = False,
) -> Optional[Union[Any, Lexicon]]:
    """Get a lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        compute_metrics (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Lexicon]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            lexicon_name=lexicon_name,
            client=client,
            compute_metrics=compute_metrics,
        )
    ).parsed

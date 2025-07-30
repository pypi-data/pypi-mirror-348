from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_term_response_200 import GetTermResponse200
from ...models.term_identifier import TermIdentifier
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    lexicon_name: str,
    *,
    body: TermIdentifier,
    term_only: Union[Unset, bool] = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["termOnly"] = term_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/lexicons/{lexicon_name}/_get_term".format(
            project_name=project_name,
            lexicon_name=lexicon_name,
        ),
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetTermResponse200]:
    if response.status_code == 200:
        response_200 = GetTermResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetTermResponse200]:
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
    body: TermIdentifier,
    term_only: Union[Unset, bool] = False,
) -> Response[GetTermResponse200]:
    """Get a term from a lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        term_only (Union[Unset, bool]):  Default: False.
        body (TermIdentifier):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetTermResponse200]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        lexicon_name=lexicon_name,
        body=body,
        term_only=term_only,
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
    body: TermIdentifier,
    term_only: Union[Unset, bool] = False,
) -> Optional[GetTermResponse200]:
    """Get a term from a lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        term_only (Union[Unset, bool]):  Default: False.
        body (TermIdentifier):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetTermResponse200
    """

    return sync_detailed(
        project_name=project_name,
        lexicon_name=lexicon_name,
        client=client,
        body=body,
        term_only=term_only,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    lexicon_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: TermIdentifier,
    term_only: Union[Unset, bool] = False,
) -> Response[GetTermResponse200]:
    """Get a term from a lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        term_only (Union[Unset, bool]):  Default: False.
        body (TermIdentifier):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetTermResponse200]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        lexicon_name=lexicon_name,
        body=body,
        term_only=term_only,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    lexicon_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: TermIdentifier,
    term_only: Union[Unset, bool] = False,
) -> Optional[GetTermResponse200]:
    """Get a term from a lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        term_only (Union[Unset, bool]):  Default: False.
        body (TermIdentifier):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetTermResponse200
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            lexicon_name=lexicon_name,
            client=client,
            body=body,
            term_only=term_only,
        )
    ).parsed

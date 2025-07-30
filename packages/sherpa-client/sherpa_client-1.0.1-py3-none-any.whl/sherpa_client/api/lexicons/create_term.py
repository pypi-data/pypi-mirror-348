from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_term_body import CreateTermBody
from ...models.create_term_response_200 import CreateTermResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    lexicon_name: str,
    *,
    body: CreateTermBody,
    overwrite: Union[Unset, bool] = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["overwrite"] = overwrite

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/lexicons/{lexicon_name}".format(
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
) -> Optional[CreateTermResponse200]:
    if response.status_code == 200:
        response_200 = CreateTermResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CreateTermResponse200]:
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
    body: CreateTermBody,
    overwrite: Union[Unset, bool] = False,
) -> Response[CreateTermResponse200]:
    """Create a new term in the lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        overwrite (Union[Unset, bool]):  Default: False.
        body (CreateTermBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTermResponse200]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        lexicon_name=lexicon_name,
        body=body,
        overwrite=overwrite,
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
    body: CreateTermBody,
    overwrite: Union[Unset, bool] = False,
) -> Optional[CreateTermResponse200]:
    """Create a new term in the lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        overwrite (Union[Unset, bool]):  Default: False.
        body (CreateTermBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateTermResponse200
    """

    return sync_detailed(
        project_name=project_name,
        lexicon_name=lexicon_name,
        client=client,
        body=body,
        overwrite=overwrite,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    lexicon_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateTermBody,
    overwrite: Union[Unset, bool] = False,
) -> Response[CreateTermResponse200]:
    """Create a new term in the lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        overwrite (Union[Unset, bool]):  Default: False.
        body (CreateTermBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTermResponse200]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        lexicon_name=lexicon_name,
        body=body,
        overwrite=overwrite,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    lexicon_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateTermBody,
    overwrite: Union[Unset, bool] = False,
) -> Optional[CreateTermResponse200]:
    """Create a new term in the lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        overwrite (Union[Unset, bool]):  Default: False.
        body (CreateTermBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateTermResponse200
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            lexicon_name=lexicon_name,
            client=client,
            body=body,
            overwrite=overwrite,
        )
    ).parsed

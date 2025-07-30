from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.create_term_json_body import CreateTermJsonBody
from ...models.create_term_response_200 import CreateTermResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
    json_body: CreateTermJsonBody,
    overwrite: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/lexicons/{lexiconName}".format(
        client.base_url, projectName=project_name, lexiconName=lexicon_name
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["overwrite"] = overwrite

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[CreateTermResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateTermResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[CreateTermResponse200]:
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
    client: Client,
    json_body: CreateTermJsonBody,
    overwrite: Union[Unset, None, bool] = False,
) -> Response[CreateTermResponse200]:
    """Create a new term in the lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        overwrite (Union[Unset, None, bool]):
        json_body (CreateTermJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTermResponse200]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        lexicon_name=lexicon_name,
        client=client,
        json_body=json_body,
        overwrite=overwrite,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
    json_body: CreateTermJsonBody,
    overwrite: Union[Unset, None, bool] = False,
) -> Optional[CreateTermResponse200]:
    """Create a new term in the lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        overwrite (Union[Unset, None, bool]):
        json_body (CreateTermJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTermResponse200]
    """

    return sync_detailed(
        project_name=project_name,
        lexicon_name=lexicon_name,
        client=client,
        json_body=json_body,
        overwrite=overwrite,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
    json_body: CreateTermJsonBody,
    overwrite: Union[Unset, None, bool] = False,
) -> Response[CreateTermResponse200]:
    """Create a new term in the lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        overwrite (Union[Unset, None, bool]):
        json_body (CreateTermJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTermResponse200]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        lexicon_name=lexicon_name,
        client=client,
        json_body=json_body,
        overwrite=overwrite,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    lexicon_name: str,
    *,
    client: Client,
    json_body: CreateTermJsonBody,
    overwrite: Union[Unset, None, bool] = False,
) -> Optional[CreateTermResponse200]:
    """Create a new term in the lexicon

    Args:
        project_name (str):
        lexicon_name (str):
        overwrite (Union[Unset, None, bool]):
        json_body (CreateTermJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTermResponse200]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            lexicon_name=lexicon_name,
            client=client,
            json_body=json_body,
            overwrite=overwrite,
        )
    ).parsed

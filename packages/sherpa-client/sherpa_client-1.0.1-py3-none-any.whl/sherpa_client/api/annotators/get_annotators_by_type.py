from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.annotator_multimap import AnnotatorMultimap
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    use_cache: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["useCache"] = use_cache

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_name}/annotators_by_type".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AnnotatorMultimap]:
    if response.status_code == 200:
        response_200 = AnnotatorMultimap.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AnnotatorMultimap]:
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
    use_cache: Union[Unset, bool] = False,
) -> Response[AnnotatorMultimap]:
    """List annotators by type

    Args:
        project_name (str):
        use_cache (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotatorMultimap]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        use_cache=use_cache,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    use_cache: Union[Unset, bool] = False,
) -> Optional[AnnotatorMultimap]:
    """List annotators by type

    Args:
        project_name (str):
        use_cache (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnnotatorMultimap
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        use_cache=use_cache,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    use_cache: Union[Unset, bool] = False,
) -> Response[AnnotatorMultimap]:
    """List annotators by type

    Args:
        project_name (str):
        use_cache (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotatorMultimap]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        use_cache=use_cache,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    use_cache: Union[Unset, bool] = False,
) -> Optional[AnnotatorMultimap]:
    """List annotators by type

    Args:
        project_name (str):
        use_cache (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnnotatorMultimap
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            use_cache=use_cache,
        )
    ).parsed

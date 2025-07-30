from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.corpus_metrics import CorpusMetrics
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    compute_facets: Union[Unset, bool] = True,
    facet: Union[Unset, str] = "",
    compute_corpus_size: Union[Unset, bool] = True,
    estimated_counts: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["computeFacets"] = compute_facets

    params["facet"] = facet

    params["computeCorpusSize"] = compute_corpus_size

    params["estimatedCounts"] = estimated_counts

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_name}/corpusMetrics".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CorpusMetrics]:
    if response.status_code == 200:
        response_200 = CorpusMetrics.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CorpusMetrics]:
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
    compute_facets: Union[Unset, bool] = True,
    facet: Union[Unset, str] = "",
    compute_corpus_size: Union[Unset, bool] = True,
    estimated_counts: Union[Unset, bool] = False,
) -> Response[CorpusMetrics]:
    """Get some metrics on corpus

    Args:
        project_name (str):
        compute_facets (Union[Unset, bool]):  Default: True.
        facet (Union[Unset, str]):  Default: ''.
        compute_corpus_size (Union[Unset, bool]):  Default: True.
        estimated_counts (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CorpusMetrics]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        compute_facets=compute_facets,
        facet=facet,
        compute_corpus_size=compute_corpus_size,
        estimated_counts=estimated_counts,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_facets: Union[Unset, bool] = True,
    facet: Union[Unset, str] = "",
    compute_corpus_size: Union[Unset, bool] = True,
    estimated_counts: Union[Unset, bool] = False,
) -> Optional[CorpusMetrics]:
    """Get some metrics on corpus

    Args:
        project_name (str):
        compute_facets (Union[Unset, bool]):  Default: True.
        facet (Union[Unset, str]):  Default: ''.
        compute_corpus_size (Union[Unset, bool]):  Default: True.
        estimated_counts (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CorpusMetrics
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        compute_facets=compute_facets,
        facet=facet,
        compute_corpus_size=compute_corpus_size,
        estimated_counts=estimated_counts,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_facets: Union[Unset, bool] = True,
    facet: Union[Unset, str] = "",
    compute_corpus_size: Union[Unset, bool] = True,
    estimated_counts: Union[Unset, bool] = False,
) -> Response[CorpusMetrics]:
    """Get some metrics on corpus

    Args:
        project_name (str):
        compute_facets (Union[Unset, bool]):  Default: True.
        facet (Union[Unset, str]):  Default: ''.
        compute_corpus_size (Union[Unset, bool]):  Default: True.
        estimated_counts (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CorpusMetrics]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        compute_facets=compute_facets,
        facet=facet,
        compute_corpus_size=compute_corpus_size,
        estimated_counts=estimated_counts,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    compute_facets: Union[Unset, bool] = True,
    facet: Union[Unset, str] = "",
    compute_corpus_size: Union[Unset, bool] = True,
    estimated_counts: Union[Unset, bool] = False,
) -> Optional[CorpusMetrics]:
    """Get some metrics on corpus

    Args:
        project_name (str):
        compute_facets (Union[Unset, bool]):  Default: True.
        facet (Union[Unset, str]):  Default: ''.
        compute_corpus_size (Union[Unset, bool]):  Default: True.
        estimated_counts (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CorpusMetrics
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            compute_facets=compute_facets,
            facet=facet,
            compute_corpus_size=compute_corpus_size,
            estimated_counts=estimated_counts,
        )
    ).parsed

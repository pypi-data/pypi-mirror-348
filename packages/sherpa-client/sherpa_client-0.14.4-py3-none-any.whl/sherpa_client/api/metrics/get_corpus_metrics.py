from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.corpus_metrics import CorpusMetrics
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    compute_facets: Union[Unset, None, bool] = True,
    facet: Union[Unset, None, str] = "",
    compute_corpus_size: Union[Unset, None, bool] = True,
    estimated_counts: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/corpusMetrics".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["computeFacets"] = compute_facets

    params["facet"] = facet

    params["computeCorpusSize"] = compute_corpus_size

    params["estimatedCounts"] = estimated_counts

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[CorpusMetrics]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CorpusMetrics.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[CorpusMetrics]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    *,
    client: Client,
    compute_facets: Union[Unset, None, bool] = True,
    facet: Union[Unset, None, str] = "",
    compute_corpus_size: Union[Unset, None, bool] = True,
    estimated_counts: Union[Unset, None, bool] = False,
) -> Response[CorpusMetrics]:
    """Get some metrics on corpus

    Args:
        project_name (str):
        compute_facets (Union[Unset, None, bool]):  Default: True.
        facet (Union[Unset, None, str]):  Default: ''.
        compute_corpus_size (Union[Unset, None, bool]):  Default: True.
        estimated_counts (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CorpusMetrics]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        compute_facets=compute_facets,
        facet=facet,
        compute_corpus_size=compute_corpus_size,
        estimated_counts=estimated_counts,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Client,
    compute_facets: Union[Unset, None, bool] = True,
    facet: Union[Unset, None, str] = "",
    compute_corpus_size: Union[Unset, None, bool] = True,
    estimated_counts: Union[Unset, None, bool] = False,
) -> Optional[CorpusMetrics]:
    """Get some metrics on corpus

    Args:
        project_name (str):
        compute_facets (Union[Unset, None, bool]):  Default: True.
        facet (Union[Unset, None, str]):  Default: ''.
        compute_corpus_size (Union[Unset, None, bool]):  Default: True.
        estimated_counts (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CorpusMetrics]
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
    client: Client,
    compute_facets: Union[Unset, None, bool] = True,
    facet: Union[Unset, None, str] = "",
    compute_corpus_size: Union[Unset, None, bool] = True,
    estimated_counts: Union[Unset, None, bool] = False,
) -> Response[CorpusMetrics]:
    """Get some metrics on corpus

    Args:
        project_name (str):
        compute_facets (Union[Unset, None, bool]):  Default: True.
        facet (Union[Unset, None, str]):  Default: ''.
        compute_corpus_size (Union[Unset, None, bool]):  Default: True.
        estimated_counts (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CorpusMetrics]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        compute_facets=compute_facets,
        facet=facet,
        compute_corpus_size=compute_corpus_size,
        estimated_counts=estimated_counts,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    compute_facets: Union[Unset, None, bool] = True,
    facet: Union[Unset, None, str] = "",
    compute_corpus_size: Union[Unset, None, bool] = True,
    estimated_counts: Union[Unset, None, bool] = False,
) -> Optional[CorpusMetrics]:
    """Get some metrics on corpus

    Args:
        project_name (str):
        compute_facets (Union[Unset, None, bool]):  Default: True.
        facet (Union[Unset, None, str]):  Default: ''.
        compute_corpus_size (Union[Unset, None, bool]):  Default: True.
        estimated_counts (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CorpusMetrics]
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

from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sherpa_job_bean import SherpaJobBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    status_filter: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["statusFilter"] = status_filter

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_name}/jobs".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["SherpaJobBean"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_sherpa_job_bean_array_item_data in _response_200:
            componentsschemas_sherpa_job_bean_array_item = SherpaJobBean.from_dict(
                componentsschemas_sherpa_job_bean_array_item_data
            )

            response_200.append(componentsschemas_sherpa_job_bean_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["SherpaJobBean"]]:
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
    status_filter: Union[Unset, str] = UNSET,
) -> Response[list["SherpaJobBean"]]:
    """Get current jobs

    Args:
        project_name (str):
        status_filter (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['SherpaJobBean']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        status_filter=status_filter,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    status_filter: Union[Unset, str] = UNSET,
) -> Optional[list["SherpaJobBean"]]:
    """Get current jobs

    Args:
        project_name (str):
        status_filter (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SherpaJobBean']
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        status_filter=status_filter,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    status_filter: Union[Unset, str] = UNSET,
) -> Response[list["SherpaJobBean"]]:
    """Get current jobs

    Args:
        project_name (str):
        status_filter (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['SherpaJobBean']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        status_filter=status_filter,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    status_filter: Union[Unset, str] = UNSET,
) -> Optional[list["SherpaJobBean"]]:
    """Get current jobs

    Args:
        project_name (str):
        status_filter (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SherpaJobBean']
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            status_filter=status_filter,
        )
    ).parsed

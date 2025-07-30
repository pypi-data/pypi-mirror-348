from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.maybe_create_projects_and_import_models_from_archive_multipart_data import (
    MaybeCreateProjectsAndImportModelsFromArchiveMultipartData,
)
from ...models.project_status import ProjectStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    multipart_data: MaybeCreateProjectsAndImportModelsFromArchiveMultipartData,
    group_name: Union[Unset, None, str] = UNSET,
    reuse_project_name: Union[Unset, None, bool] = False,
    project_name: Union[Unset, None, str] = UNSET,
    project_label: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/projects/_import_models".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["groupName"] = group_name

    params["reuseProjectName"] = reuse_project_name

    params["projectName"] = project_name

    params["projectLabel"] = project_label

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[List["ProjectStatus"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_project_status_array_item_data in _response_200:
            componentsschemas_project_status_array_item = ProjectStatus.from_dict(
                componentsschemas_project_status_array_item_data
            )

            response_200.append(componentsschemas_project_status_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[List["ProjectStatus"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    multipart_data: MaybeCreateProjectsAndImportModelsFromArchiveMultipartData,
    group_name: Union[Unset, None, str] = UNSET,
    reuse_project_name: Union[Unset, None, bool] = False,
    project_name: Union[Unset, None, str] = UNSET,
    project_label: Union[Unset, None, str] = UNSET,
) -> Response[List["ProjectStatus"]]:
    """import models (and create projects if required)

    Args:
        group_name (Union[Unset, None, str]):
        reuse_project_name (Union[Unset, None, bool]):
        project_name (Union[Unset, None, str]):
        project_label (Union[Unset, None, str]):
        multipart_data (MaybeCreateProjectsAndImportModelsFromArchiveMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ProjectStatus']]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        group_name=group_name,
        reuse_project_name=reuse_project_name,
        project_name=project_name,
        project_label=project_label,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    multipart_data: MaybeCreateProjectsAndImportModelsFromArchiveMultipartData,
    group_name: Union[Unset, None, str] = UNSET,
    reuse_project_name: Union[Unset, None, bool] = False,
    project_name: Union[Unset, None, str] = UNSET,
    project_label: Union[Unset, None, str] = UNSET,
) -> Optional[List["ProjectStatus"]]:
    """import models (and create projects if required)

    Args:
        group_name (Union[Unset, None, str]):
        reuse_project_name (Union[Unset, None, bool]):
        project_name (Union[Unset, None, str]):
        project_label (Union[Unset, None, str]):
        multipart_data (MaybeCreateProjectsAndImportModelsFromArchiveMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ProjectStatus']]
    """

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
        group_name=group_name,
        reuse_project_name=reuse_project_name,
        project_name=project_name,
        project_label=project_label,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    multipart_data: MaybeCreateProjectsAndImportModelsFromArchiveMultipartData,
    group_name: Union[Unset, None, str] = UNSET,
    reuse_project_name: Union[Unset, None, bool] = False,
    project_name: Union[Unset, None, str] = UNSET,
    project_label: Union[Unset, None, str] = UNSET,
) -> Response[List["ProjectStatus"]]:
    """import models (and create projects if required)

    Args:
        group_name (Union[Unset, None, str]):
        reuse_project_name (Union[Unset, None, bool]):
        project_name (Union[Unset, None, str]):
        project_label (Union[Unset, None, str]):
        multipart_data (MaybeCreateProjectsAndImportModelsFromArchiveMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ProjectStatus']]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        group_name=group_name,
        reuse_project_name=reuse_project_name,
        project_name=project_name,
        project_label=project_label,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    multipart_data: MaybeCreateProjectsAndImportModelsFromArchiveMultipartData,
    group_name: Union[Unset, None, str] = UNSET,
    reuse_project_name: Union[Unset, None, bool] = False,
    project_name: Union[Unset, None, str] = UNSET,
    project_label: Union[Unset, None, str] = UNSET,
) -> Optional[List["ProjectStatus"]]:
    """import models (and create projects if required)

    Args:
        group_name (Union[Unset, None, str]):
        reuse_project_name (Union[Unset, None, bool]):
        project_name (Union[Unset, None, str]):
        project_label (Union[Unset, None, str]):
        multipart_data (MaybeCreateProjectsAndImportModelsFromArchiveMultipartData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ProjectStatus']]
    """

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
            group_name=group_name,
            reuse_project_name=reuse_project_name,
            project_name=project_name,
            project_label=project_label,
        )
    ).parsed

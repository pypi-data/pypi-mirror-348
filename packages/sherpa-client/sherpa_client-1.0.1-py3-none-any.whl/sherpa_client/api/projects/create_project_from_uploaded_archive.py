from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sherpa_job_bean import SherpaJobBean
from ...models.uploaded_file import UploadedFile
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: UploadedFile,
    group_name: Union[Unset, str] = UNSET,
    reuse_project_name: Union[Unset, bool] = False,
    project_name: Union[Unset, str] = UNSET,
    project_label: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["groupName"] = group_name

    params["reuseProjectName"] = reuse_project_name

    params["projectName"] = project_name

    params["projectLabel"] = project_label

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/_load",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SherpaJobBean]:
    if response.status_code == 200:
        response_200 = SherpaJobBean.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SherpaJobBean]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadedFile,
    group_name: Union[Unset, str] = UNSET,
    reuse_project_name: Union[Unset, bool] = False,
    project_name: Union[Unset, str] = UNSET,
    project_label: Union[Unset, str] = UNSET,
) -> Response[SherpaJobBean]:
    """create a project from an already uploaded archive

    Args:
        group_name (Union[Unset, str]):
        reuse_project_name (Union[Unset, bool]):  Default: False.
        project_name (Union[Unset, str]):
        project_label (Union[Unset, str]):
        body (UploadedFile):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        body=body,
        group_name=group_name,
        reuse_project_name=reuse_project_name,
        project_name=project_name,
        project_label=project_label,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadedFile,
    group_name: Union[Unset, str] = UNSET,
    reuse_project_name: Union[Unset, bool] = False,
    project_name: Union[Unset, str] = UNSET,
    project_label: Union[Unset, str] = UNSET,
) -> Optional[SherpaJobBean]:
    """create a project from an already uploaded archive

    Args:
        group_name (Union[Unset, str]):
        reuse_project_name (Union[Unset, bool]):  Default: False.
        project_name (Union[Unset, str]):
        project_label (Union[Unset, str]):
        body (UploadedFile):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SherpaJobBean
    """

    return sync_detailed(
        client=client,
        body=body,
        group_name=group_name,
        reuse_project_name=reuse_project_name,
        project_name=project_name,
        project_label=project_label,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadedFile,
    group_name: Union[Unset, str] = UNSET,
    reuse_project_name: Union[Unset, bool] = False,
    project_name: Union[Unset, str] = UNSET,
    project_label: Union[Unset, str] = UNSET,
) -> Response[SherpaJobBean]:
    """create a project from an already uploaded archive

    Args:
        group_name (Union[Unset, str]):
        reuse_project_name (Union[Unset, bool]):  Default: False.
        project_name (Union[Unset, str]):
        project_label (Union[Unset, str]):
        body (UploadedFile):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        body=body,
        group_name=group_name,
        reuse_project_name=reuse_project_name,
        project_name=project_name,
        project_label=project_label,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadedFile,
    group_name: Union[Unset, str] = UNSET,
    reuse_project_name: Union[Unset, bool] = False,
    project_name: Union[Unset, str] = UNSET,
    project_label: Union[Unset, str] = UNSET,
) -> Optional[SherpaJobBean]:
    """create a project from an already uploaded archive

    Args:
        group_name (Union[Unset, str]):
        reuse_project_name (Union[Unset, bool]):  Default: False.
        project_name (Union[Unset, str]):
        project_label (Union[Unset, str]):
        body (UploadedFile):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SherpaJobBean
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            group_name=group_name,
            reuse_project_name=reuse_project_name,
            project_name=project_name,
            project_label=project_label,
        )
    ).parsed

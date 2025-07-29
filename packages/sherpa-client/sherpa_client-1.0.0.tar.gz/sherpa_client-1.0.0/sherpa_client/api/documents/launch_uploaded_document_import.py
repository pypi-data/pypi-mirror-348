from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.launch_uploaded_document_import_segmentation_policy import (
    LaunchUploadedDocumentImportSegmentationPolicy,
)
from ...models.sherpa_job_bean import SherpaJobBean
from ...models.uploaded_file import UploadedFile
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    body: list["UploadedFile"],
    ignore_labelling: Union[Unset, bool] = False,
    segmentation_policy: Union[
        Unset, LaunchUploadedDocumentImportSegmentationPolicy
    ] = LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, bool] = False,
    clean_text: Union[Unset, bool] = True,
    generate_categories_from_source_folder: Union[Unset, bool] = False,
    group_name: Union[Unset, str] = UNSET,
    idp_group_identifier: Union[Unset, str] = UNSET,
    wait: Union[Unset, bool] = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["ignoreLabelling"] = ignore_labelling

    json_segmentation_policy: Union[Unset, str] = UNSET
    if not isinstance(segmentation_policy, Unset):
        json_segmentation_policy = segmentation_policy.value

    params["segmentationPolicy"] = json_segmentation_policy

    params["splitCorpus"] = split_corpus

    params["cleanText"] = clean_text

    params["generateCategoriesFromSourceFolder"] = (
        generate_categories_from_source_folder
    )

    params["groupName"] = group_name

    params["idpGroupIdentifier"] = idp_group_identifier

    params["wait"] = wait

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/documents/_load".format(
            project_name=project_name,
        ),
        "params": params,
    }

    _body = []
    for componentsschemas_uploaded_file_array_item_data in body:
        componentsschemas_uploaded_file_array_item = (
            componentsschemas_uploaded_file_array_item_data.to_dict()
        )
        _body.append(componentsschemas_uploaded_file_array_item)

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
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["UploadedFile"],
    ignore_labelling: Union[Unset, bool] = False,
    segmentation_policy: Union[
        Unset, LaunchUploadedDocumentImportSegmentationPolicy
    ] = LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, bool] = False,
    clean_text: Union[Unset, bool] = True,
    generate_categories_from_source_folder: Union[Unset, bool] = False,
    group_name: Union[Unset, str] = UNSET,
    idp_group_identifier: Union[Unset, str] = UNSET,
    wait: Union[Unset, bool] = False,
) -> Response[SherpaJobBean]:
    """import documents already uploaded on the server into the project

    Args:
        project_name (str):
        ignore_labelling (Union[Unset, bool]):  Default: False.
        segmentation_policy (Union[Unset, LaunchUploadedDocumentImportSegmentationPolicy]):
            Default: LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING.
        split_corpus (Union[Unset, bool]):  Default: False.
        clean_text (Union[Unset, bool]):  Default: True.
        generate_categories_from_source_folder (Union[Unset, bool]):  Default: False.
        group_name (Union[Unset, str]):
        idp_group_identifier (Union[Unset, str]):
        wait (Union[Unset, bool]):  Default: False.
        body (list['UploadedFile']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        body=body,
        ignore_labelling=ignore_labelling,
        segmentation_policy=segmentation_policy,
        split_corpus=split_corpus,
        clean_text=clean_text,
        generate_categories_from_source_folder=generate_categories_from_source_folder,
        group_name=group_name,
        idp_group_identifier=idp_group_identifier,
        wait=wait,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["UploadedFile"],
    ignore_labelling: Union[Unset, bool] = False,
    segmentation_policy: Union[
        Unset, LaunchUploadedDocumentImportSegmentationPolicy
    ] = LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, bool] = False,
    clean_text: Union[Unset, bool] = True,
    generate_categories_from_source_folder: Union[Unset, bool] = False,
    group_name: Union[Unset, str] = UNSET,
    idp_group_identifier: Union[Unset, str] = UNSET,
    wait: Union[Unset, bool] = False,
) -> Optional[SherpaJobBean]:
    """import documents already uploaded on the server into the project

    Args:
        project_name (str):
        ignore_labelling (Union[Unset, bool]):  Default: False.
        segmentation_policy (Union[Unset, LaunchUploadedDocumentImportSegmentationPolicy]):
            Default: LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING.
        split_corpus (Union[Unset, bool]):  Default: False.
        clean_text (Union[Unset, bool]):  Default: True.
        generate_categories_from_source_folder (Union[Unset, bool]):  Default: False.
        group_name (Union[Unset, str]):
        idp_group_identifier (Union[Unset, str]):
        wait (Union[Unset, bool]):  Default: False.
        body (list['UploadedFile']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SherpaJobBean
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        body=body,
        ignore_labelling=ignore_labelling,
        segmentation_policy=segmentation_policy,
        split_corpus=split_corpus,
        clean_text=clean_text,
        generate_categories_from_source_folder=generate_categories_from_source_folder,
        group_name=group_name,
        idp_group_identifier=idp_group_identifier,
        wait=wait,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["UploadedFile"],
    ignore_labelling: Union[Unset, bool] = False,
    segmentation_policy: Union[
        Unset, LaunchUploadedDocumentImportSegmentationPolicy
    ] = LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, bool] = False,
    clean_text: Union[Unset, bool] = True,
    generate_categories_from_source_folder: Union[Unset, bool] = False,
    group_name: Union[Unset, str] = UNSET,
    idp_group_identifier: Union[Unset, str] = UNSET,
    wait: Union[Unset, bool] = False,
) -> Response[SherpaJobBean]:
    """import documents already uploaded on the server into the project

    Args:
        project_name (str):
        ignore_labelling (Union[Unset, bool]):  Default: False.
        segmentation_policy (Union[Unset, LaunchUploadedDocumentImportSegmentationPolicy]):
            Default: LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING.
        split_corpus (Union[Unset, bool]):  Default: False.
        clean_text (Union[Unset, bool]):  Default: True.
        generate_categories_from_source_folder (Union[Unset, bool]):  Default: False.
        group_name (Union[Unset, str]):
        idp_group_identifier (Union[Unset, str]):
        wait (Union[Unset, bool]):  Default: False.
        body (list['UploadedFile']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        body=body,
        ignore_labelling=ignore_labelling,
        segmentation_policy=segmentation_policy,
        split_corpus=split_corpus,
        clean_text=clean_text,
        generate_categories_from_source_folder=generate_categories_from_source_folder,
        group_name=group_name,
        idp_group_identifier=idp_group_identifier,
        wait=wait,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["UploadedFile"],
    ignore_labelling: Union[Unset, bool] = False,
    segmentation_policy: Union[
        Unset, LaunchUploadedDocumentImportSegmentationPolicy
    ] = LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, bool] = False,
    clean_text: Union[Unset, bool] = True,
    generate_categories_from_source_folder: Union[Unset, bool] = False,
    group_name: Union[Unset, str] = UNSET,
    idp_group_identifier: Union[Unset, str] = UNSET,
    wait: Union[Unset, bool] = False,
) -> Optional[SherpaJobBean]:
    """import documents already uploaded on the server into the project

    Args:
        project_name (str):
        ignore_labelling (Union[Unset, bool]):  Default: False.
        segmentation_policy (Union[Unset, LaunchUploadedDocumentImportSegmentationPolicy]):
            Default: LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING.
        split_corpus (Union[Unset, bool]):  Default: False.
        clean_text (Union[Unset, bool]):  Default: True.
        generate_categories_from_source_folder (Union[Unset, bool]):  Default: False.
        group_name (Union[Unset, str]):
        idp_group_identifier (Union[Unset, str]):
        wait (Union[Unset, bool]):  Default: False.
        body (list['UploadedFile']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SherpaJobBean
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            body=body,
            ignore_labelling=ignore_labelling,
            segmentation_policy=segmentation_policy,
            split_corpus=split_corpus,
            clean_text=clean_text,
            generate_categories_from_source_folder=generate_categories_from_source_folder,
            group_name=group_name,
            idp_group_identifier=idp_group_identifier,
            wait=wait,
        )
    ).parsed

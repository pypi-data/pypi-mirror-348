from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.launch_uploaded_document_import_clean_text import LaunchUploadedDocumentImportCleanText
from ...models.launch_uploaded_document_import_segmentation_policy import LaunchUploadedDocumentImportSegmentationPolicy
from ...models.sherpa_job_bean import SherpaJobBean
from ...models.uploaded_file import UploadedFile
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    json_body: List["UploadedFile"],
    ignore_labelling: Union[Unset, None, bool] = False,
    segmentation_policy: Union[
        Unset, None, LaunchUploadedDocumentImportSegmentationPolicy
    ] = LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, None, bool] = False,
    clean_text: Union[
        Unset, None, LaunchUploadedDocumentImportCleanText
    ] = LaunchUploadedDocumentImportCleanText.DEFAULT,
    generate_categories_from_source_folder: Union[Unset, None, bool] = False,
    group_name: Union[Unset, None, str] = UNSET,
    idp_group_identifier: Union[Unset, None, str] = UNSET,
    wait: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/documents/_load".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ignoreLabelling"] = ignore_labelling

    json_segmentation_policy: Union[Unset, None, str] = UNSET
    if not isinstance(segmentation_policy, Unset):
        json_segmentation_policy = segmentation_policy.value if segmentation_policy else None

    params["segmentationPolicy"] = json_segmentation_policy

    params["splitCorpus"] = split_corpus

    json_clean_text: Union[Unset, None, str] = UNSET
    if not isinstance(clean_text, Unset):
        json_clean_text = clean_text.value if clean_text else None

    params["cleanText"] = json_clean_text

    params["generateCategoriesFromSourceFolder"] = generate_categories_from_source_folder

    params["groupName"] = group_name

    params["idpGroupIdentifier"] = idp_group_identifier

    params["wait"] = wait

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = []
    for componentsschemas_uploaded_file_array_item_data in json_body:
        componentsschemas_uploaded_file_array_item = componentsschemas_uploaded_file_array_item_data.to_dict()

        json_json_body.append(componentsschemas_uploaded_file_array_item)

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[SherpaJobBean]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SherpaJobBean.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[SherpaJobBean]:
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
    json_body: List["UploadedFile"],
    ignore_labelling: Union[Unset, None, bool] = False,
    segmentation_policy: Union[
        Unset, None, LaunchUploadedDocumentImportSegmentationPolicy
    ] = LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, None, bool] = False,
    clean_text: Union[
        Unset, None, LaunchUploadedDocumentImportCleanText
    ] = LaunchUploadedDocumentImportCleanText.DEFAULT,
    generate_categories_from_source_folder: Union[Unset, None, bool] = False,
    group_name: Union[Unset, None, str] = UNSET,
    idp_group_identifier: Union[Unset, None, str] = UNSET,
    wait: Union[Unset, None, bool] = False,
) -> Response[SherpaJobBean]:
    """import documents already uploaded on the server into the project

    Args:
        project_name (str):
        ignore_labelling (Union[Unset, None, bool]):
        segmentation_policy (Union[Unset, None, LaunchUploadedDocumentImportSegmentationPolicy]):
            Default: LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING.
        split_corpus (Union[Unset, None, bool]):
        clean_text (Union[Unset, None, LaunchUploadedDocumentImportCleanText]):  Default:
            LaunchUploadedDocumentImportCleanText.DEFAULT.
        generate_categories_from_source_folder (Union[Unset, None, bool]):
        group_name (Union[Unset, None, str]):
        idp_group_identifier (Union[Unset, None, str]):
        wait (Union[Unset, None, bool]):
        json_body (List['UploadedFile']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        json_body=json_body,
        ignore_labelling=ignore_labelling,
        segmentation_policy=segmentation_policy,
        split_corpus=split_corpus,
        clean_text=clean_text,
        generate_categories_from_source_folder=generate_categories_from_source_folder,
        group_name=group_name,
        idp_group_identifier=idp_group_identifier,
        wait=wait,
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
    json_body: List["UploadedFile"],
    ignore_labelling: Union[Unset, None, bool] = False,
    segmentation_policy: Union[
        Unset, None, LaunchUploadedDocumentImportSegmentationPolicy
    ] = LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, None, bool] = False,
    clean_text: Union[
        Unset, None, LaunchUploadedDocumentImportCleanText
    ] = LaunchUploadedDocumentImportCleanText.DEFAULT,
    generate_categories_from_source_folder: Union[Unset, None, bool] = False,
    group_name: Union[Unset, None, str] = UNSET,
    idp_group_identifier: Union[Unset, None, str] = UNSET,
    wait: Union[Unset, None, bool] = False,
) -> Optional[SherpaJobBean]:
    """import documents already uploaded on the server into the project

    Args:
        project_name (str):
        ignore_labelling (Union[Unset, None, bool]):
        segmentation_policy (Union[Unset, None, LaunchUploadedDocumentImportSegmentationPolicy]):
            Default: LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING.
        split_corpus (Union[Unset, None, bool]):
        clean_text (Union[Unset, None, LaunchUploadedDocumentImportCleanText]):  Default:
            LaunchUploadedDocumentImportCleanText.DEFAULT.
        generate_categories_from_source_folder (Union[Unset, None, bool]):
        group_name (Union[Unset, None, str]):
        idp_group_identifier (Union[Unset, None, str]):
        wait (Union[Unset, None, bool]):
        json_body (List['UploadedFile']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        json_body=json_body,
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
    client: Client,
    json_body: List["UploadedFile"],
    ignore_labelling: Union[Unset, None, bool] = False,
    segmentation_policy: Union[
        Unset, None, LaunchUploadedDocumentImportSegmentationPolicy
    ] = LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, None, bool] = False,
    clean_text: Union[
        Unset, None, LaunchUploadedDocumentImportCleanText
    ] = LaunchUploadedDocumentImportCleanText.DEFAULT,
    generate_categories_from_source_folder: Union[Unset, None, bool] = False,
    group_name: Union[Unset, None, str] = UNSET,
    idp_group_identifier: Union[Unset, None, str] = UNSET,
    wait: Union[Unset, None, bool] = False,
) -> Response[SherpaJobBean]:
    """import documents already uploaded on the server into the project

    Args:
        project_name (str):
        ignore_labelling (Union[Unset, None, bool]):
        segmentation_policy (Union[Unset, None, LaunchUploadedDocumentImportSegmentationPolicy]):
            Default: LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING.
        split_corpus (Union[Unset, None, bool]):
        clean_text (Union[Unset, None, LaunchUploadedDocumentImportCleanText]):  Default:
            LaunchUploadedDocumentImportCleanText.DEFAULT.
        generate_categories_from_source_folder (Union[Unset, None, bool]):
        group_name (Union[Unset, None, str]):
        idp_group_identifier (Union[Unset, None, str]):
        wait (Union[Unset, None, bool]):
        json_body (List['UploadedFile']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        json_body=json_body,
        ignore_labelling=ignore_labelling,
        segmentation_policy=segmentation_policy,
        split_corpus=split_corpus,
        clean_text=clean_text,
        generate_categories_from_source_folder=generate_categories_from_source_folder,
        group_name=group_name,
        idp_group_identifier=idp_group_identifier,
        wait=wait,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    json_body: List["UploadedFile"],
    ignore_labelling: Union[Unset, None, bool] = False,
    segmentation_policy: Union[
        Unset, None, LaunchUploadedDocumentImportSegmentationPolicy
    ] = LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING,
    split_corpus: Union[Unset, None, bool] = False,
    clean_text: Union[
        Unset, None, LaunchUploadedDocumentImportCleanText
    ] = LaunchUploadedDocumentImportCleanText.DEFAULT,
    generate_categories_from_source_folder: Union[Unset, None, bool] = False,
    group_name: Union[Unset, None, str] = UNSET,
    idp_group_identifier: Union[Unset, None, str] = UNSET,
    wait: Union[Unset, None, bool] = False,
) -> Optional[SherpaJobBean]:
    """import documents already uploaded on the server into the project

    Args:
        project_name (str):
        ignore_labelling (Union[Unset, None, bool]):
        segmentation_policy (Union[Unset, None, LaunchUploadedDocumentImportSegmentationPolicy]):
            Default: LaunchUploadedDocumentImportSegmentationPolicy.COMPUTE_IF_MISSING.
        split_corpus (Union[Unset, None, bool]):
        clean_text (Union[Unset, None, LaunchUploadedDocumentImportCleanText]):  Default:
            LaunchUploadedDocumentImportCleanText.DEFAULT.
        generate_categories_from_source_folder (Union[Unset, None, bool]):
        group_name (Union[Unset, None, str]):
        idp_group_identifier (Union[Unset, None, str]):
        wait (Union[Unset, None, bool]):
        json_body (List['UploadedFile']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SherpaJobBean]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            json_body=json_body,
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

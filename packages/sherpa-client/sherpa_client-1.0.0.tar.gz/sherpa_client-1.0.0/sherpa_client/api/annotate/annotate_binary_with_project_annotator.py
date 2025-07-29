from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.annotate_binary_with_project_annotator_body import (
    AnnotateBinaryWithProjectAnnotatorBody,
)
from ...models.annotated_document import AnnotatedDocument
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    annotator: str,
    *,
    body: AnnotateBinaryWithProjectAnnotatorBody,
    inline_labels: Union[Unset, bool] = True,
    inline_label_ids: Union[Unset, bool] = True,
    inline_text: Union[Unset, bool] = True,
    debug: Union[Unset, bool] = False,
    parallelize: Union[Unset, bool] = False,
    error_policy: Union[Unset, str] = UNSET,
    output_fields: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["inlineLabels"] = inline_labels

    params["inlineLabelIds"] = inline_label_ids

    params["inlineText"] = inline_text

    params["debug"] = debug

    params["parallelize"] = parallelize

    params["errorPolicy"] = error_policy

    params["outputFields"] = output_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/annotate/projects/{project_name}/annotators/{annotator}/_annotate_binary".format(
            project_name=project_name,
            annotator=annotator,
        ),
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["AnnotatedDocument"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_annotated_document_array_item_data in _response_200:
            componentsschemas_annotated_document_array_item = (
                AnnotatedDocument.from_dict(
                    componentsschemas_annotated_document_array_item_data
                )
            )

            response_200.append(componentsschemas_annotated_document_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AnnotatedDocument"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    annotator: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AnnotateBinaryWithProjectAnnotatorBody,
    inline_labels: Union[Unset, bool] = True,
    inline_label_ids: Union[Unset, bool] = True,
    inline_text: Union[Unset, bool] = True,
    debug: Union[Unset, bool] = False,
    parallelize: Union[Unset, bool] = False,
    error_policy: Union[Unset, str] = UNSET,
    output_fields: Union[Unset, str] = UNSET,
) -> Response[list["AnnotatedDocument"]]:
    """annotate a binary document with a project annotator

    Args:
        project_name (str):
        annotator (str):
        inline_labels (Union[Unset, bool]):  Default: True.
        inline_label_ids (Union[Unset, bool]):  Default: True.
        inline_text (Union[Unset, bool]):  Default: True.
        debug (Union[Unset, bool]):  Default: False.
        parallelize (Union[Unset, bool]):  Default: False.
        error_policy (Union[Unset, str]):
        output_fields (Union[Unset, str]):
        body (AnnotateBinaryWithProjectAnnotatorBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AnnotatedDocument']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        annotator=annotator,
        body=body,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
        parallelize=parallelize,
        error_policy=error_policy,
        output_fields=output_fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    annotator: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AnnotateBinaryWithProjectAnnotatorBody,
    inline_labels: Union[Unset, bool] = True,
    inline_label_ids: Union[Unset, bool] = True,
    inline_text: Union[Unset, bool] = True,
    debug: Union[Unset, bool] = False,
    parallelize: Union[Unset, bool] = False,
    error_policy: Union[Unset, str] = UNSET,
    output_fields: Union[Unset, str] = UNSET,
) -> Optional[list["AnnotatedDocument"]]:
    """annotate a binary document with a project annotator

    Args:
        project_name (str):
        annotator (str):
        inline_labels (Union[Unset, bool]):  Default: True.
        inline_label_ids (Union[Unset, bool]):  Default: True.
        inline_text (Union[Unset, bool]):  Default: True.
        debug (Union[Unset, bool]):  Default: False.
        parallelize (Union[Unset, bool]):  Default: False.
        error_policy (Union[Unset, str]):
        output_fields (Union[Unset, str]):
        body (AnnotateBinaryWithProjectAnnotatorBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnnotatedDocument']
    """

    return sync_detailed(
        project_name=project_name,
        annotator=annotator,
        client=client,
        body=body,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
        parallelize=parallelize,
        error_policy=error_policy,
        output_fields=output_fields,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    annotator: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AnnotateBinaryWithProjectAnnotatorBody,
    inline_labels: Union[Unset, bool] = True,
    inline_label_ids: Union[Unset, bool] = True,
    inline_text: Union[Unset, bool] = True,
    debug: Union[Unset, bool] = False,
    parallelize: Union[Unset, bool] = False,
    error_policy: Union[Unset, str] = UNSET,
    output_fields: Union[Unset, str] = UNSET,
) -> Response[list["AnnotatedDocument"]]:
    """annotate a binary document with a project annotator

    Args:
        project_name (str):
        annotator (str):
        inline_labels (Union[Unset, bool]):  Default: True.
        inline_label_ids (Union[Unset, bool]):  Default: True.
        inline_text (Union[Unset, bool]):  Default: True.
        debug (Union[Unset, bool]):  Default: False.
        parallelize (Union[Unset, bool]):  Default: False.
        error_policy (Union[Unset, str]):
        output_fields (Union[Unset, str]):
        body (AnnotateBinaryWithProjectAnnotatorBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AnnotatedDocument']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        annotator=annotator,
        body=body,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
        parallelize=parallelize,
        error_policy=error_policy,
        output_fields=output_fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    annotator: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AnnotateBinaryWithProjectAnnotatorBody,
    inline_labels: Union[Unset, bool] = True,
    inline_label_ids: Union[Unset, bool] = True,
    inline_text: Union[Unset, bool] = True,
    debug: Union[Unset, bool] = False,
    parallelize: Union[Unset, bool] = False,
    error_policy: Union[Unset, str] = UNSET,
    output_fields: Union[Unset, str] = UNSET,
) -> Optional[list["AnnotatedDocument"]]:
    """annotate a binary document with a project annotator

    Args:
        project_name (str):
        annotator (str):
        inline_labels (Union[Unset, bool]):  Default: True.
        inline_label_ids (Union[Unset, bool]):  Default: True.
        inline_text (Union[Unset, bool]):  Default: True.
        debug (Union[Unset, bool]):  Default: False.
        parallelize (Union[Unset, bool]):  Default: False.
        error_policy (Union[Unset, str]):
        output_fields (Union[Unset, str]):
        body (AnnotateBinaryWithProjectAnnotatorBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnnotatedDocument']
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            annotator=annotator,
            client=client,
            body=body,
            inline_labels=inline_labels,
            inline_label_ids=inline_label_ids,
            inline_text=inline_text,
            debug=debug,
            parallelize=parallelize,
            error_policy=error_policy,
            output_fields=output_fields,
        )
    ).parsed

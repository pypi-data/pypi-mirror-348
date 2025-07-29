from http import HTTPStatus
from io import BytesIO
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.format_binary_form import FormatBinaryForm
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    *,
    body: FormatBinaryForm,
    inline_labels: Union[Unset, bool] = True,
    inline_label_ids: Union[Unset, bool] = True,
    inline_text: Union[Unset, bool] = True,
    debug: Union[Unset, bool] = False,
    parallelize: Union[Unset, bool] = False,
    error_policy: Union[Unset, str] = UNSET,
    project_context: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["inlineLabels"] = inline_labels

    params["inlineLabelIds"] = inline_label_ids

    params["inlineText"] = inline_text

    params["debug"] = debug

    params["parallelize"] = parallelize

    params["errorPolicy"] = error_policy

    params["projectContext"] = project_context

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/annotate/_annotate_format_binary",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[File]:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.json()))

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[File]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: FormatBinaryForm,
    inline_labels: Union[Unset, bool] = True,
    inline_label_ids: Union[Unset, bool] = True,
    inline_text: Union[Unset, bool] = True,
    debug: Union[Unset, bool] = False,
    parallelize: Union[Unset, bool] = False,
    error_policy: Union[Unset, str] = UNSET,
    project_context: Union[Unset, str] = UNSET,
) -> Response[File]:
    """annotate a binary document with a pipeline and return a formatted result

    Args:
        inline_labels (Union[Unset, bool]):  Default: True.
        inline_label_ids (Union[Unset, bool]):  Default: True.
        inline_text (Union[Unset, bool]):  Default: True.
        debug (Union[Unset, bool]):  Default: False.
        parallelize (Union[Unset, bool]):  Default: False.
        error_policy (Union[Unset, str]):
        project_context (Union[Unset, str]):
        body (FormatBinaryForm):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        body=body,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
        parallelize=parallelize,
        error_policy=error_policy,
        project_context=project_context,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: FormatBinaryForm,
    inline_labels: Union[Unset, bool] = True,
    inline_label_ids: Union[Unset, bool] = True,
    inline_text: Union[Unset, bool] = True,
    debug: Union[Unset, bool] = False,
    parallelize: Union[Unset, bool] = False,
    error_policy: Union[Unset, str] = UNSET,
    project_context: Union[Unset, str] = UNSET,
) -> Optional[File]:
    """annotate a binary document with a pipeline and return a formatted result

    Args:
        inline_labels (Union[Unset, bool]):  Default: True.
        inline_label_ids (Union[Unset, bool]):  Default: True.
        inline_text (Union[Unset, bool]):  Default: True.
        debug (Union[Unset, bool]):  Default: False.
        parallelize (Union[Unset, bool]):  Default: False.
        error_policy (Union[Unset, str]):
        project_context (Union[Unset, str]):
        body (FormatBinaryForm):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        File
    """

    return sync_detailed(
        client=client,
        body=body,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
        parallelize=parallelize,
        error_policy=error_policy,
        project_context=project_context,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: FormatBinaryForm,
    inline_labels: Union[Unset, bool] = True,
    inline_label_ids: Union[Unset, bool] = True,
    inline_text: Union[Unset, bool] = True,
    debug: Union[Unset, bool] = False,
    parallelize: Union[Unset, bool] = False,
    error_policy: Union[Unset, str] = UNSET,
    project_context: Union[Unset, str] = UNSET,
) -> Response[File]:
    """annotate a binary document with a pipeline and return a formatted result

    Args:
        inline_labels (Union[Unset, bool]):  Default: True.
        inline_label_ids (Union[Unset, bool]):  Default: True.
        inline_text (Union[Unset, bool]):  Default: True.
        debug (Union[Unset, bool]):  Default: False.
        parallelize (Union[Unset, bool]):  Default: False.
        error_policy (Union[Unset, str]):
        project_context (Union[Unset, str]):
        body (FormatBinaryForm):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        body=body,
        inline_labels=inline_labels,
        inline_label_ids=inline_label_ids,
        inline_text=inline_text,
        debug=debug,
        parallelize=parallelize,
        error_policy=error_policy,
        project_context=project_context,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: FormatBinaryForm,
    inline_labels: Union[Unset, bool] = True,
    inline_label_ids: Union[Unset, bool] = True,
    inline_text: Union[Unset, bool] = True,
    debug: Union[Unset, bool] = False,
    parallelize: Union[Unset, bool] = False,
    error_policy: Union[Unset, str] = UNSET,
    project_context: Union[Unset, str] = UNSET,
) -> Optional[File]:
    """annotate a binary document with a pipeline and return a formatted result

    Args:
        inline_labels (Union[Unset, bool]):  Default: True.
        inline_label_ids (Union[Unset, bool]):  Default: True.
        inline_text (Union[Unset, bool]):  Default: True.
        debug (Union[Unset, bool]):  Default: False.
        parallelize (Union[Unset, bool]):  Default: False.
        error_policy (Union[Unset, str]):
        project_context (Union[Unset, str]):
        body (FormatBinaryForm):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        File
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            inline_labels=inline_labels,
            inline_label_ids=inline_label_ids,
            inline_text=inline_text,
            debug=debug,
            parallelize=parallelize,
            error_policy=error_policy,
            project_context=project_context,
        )
    ).parsed

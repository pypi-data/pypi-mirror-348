from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.named_annotation_plan import NamedAnnotationPlan
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    tags: Union[Unset, str] = UNSET,
    include_step_dependencies: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["tags"] = tags

    params["includeStepDependencies"] = include_step_dependencies

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_name}/plans".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["NamedAnnotationPlan"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_named_annotation_plan_array_item_data in _response_200:
            componentsschemas_named_annotation_plan_array_item = (
                NamedAnnotationPlan.from_dict(
                    componentsschemas_named_annotation_plan_array_item_data
                )
            )

            response_200.append(componentsschemas_named_annotation_plan_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["NamedAnnotationPlan"]]:
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
    tags: Union[Unset, str] = UNSET,
    include_step_dependencies: Union[Unset, bool] = False,
) -> Response[list["NamedAnnotationPlan"]]:
    """List plans

    Args:
        project_name (str):
        tags (Union[Unset, str]):
        include_step_dependencies (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['NamedAnnotationPlan']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        tags=tags,
        include_step_dependencies=include_step_dependencies,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    tags: Union[Unset, str] = UNSET,
    include_step_dependencies: Union[Unset, bool] = False,
) -> Optional[list["NamedAnnotationPlan"]]:
    """List plans

    Args:
        project_name (str):
        tags (Union[Unset, str]):
        include_step_dependencies (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['NamedAnnotationPlan']
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        tags=tags,
        include_step_dependencies=include_step_dependencies,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    tags: Union[Unset, str] = UNSET,
    include_step_dependencies: Union[Unset, bool] = False,
) -> Response[list["NamedAnnotationPlan"]]:
    """List plans

    Args:
        project_name (str):
        tags (Union[Unset, str]):
        include_step_dependencies (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['NamedAnnotationPlan']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        tags=tags,
        include_step_dependencies=include_step_dependencies,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    tags: Union[Unset, str] = UNSET,
    include_step_dependencies: Union[Unset, bool] = False,
) -> Optional[list["NamedAnnotationPlan"]]:
    """List plans

    Args:
        project_name (str):
        tags (Union[Unset, str]):
        include_step_dependencies (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['NamedAnnotationPlan']
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            tags=tags,
            include_step_dependencies=include_step_dependencies,
        )
    ).parsed

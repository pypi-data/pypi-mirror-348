from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.update_building_role_dto import UpdateBuildingRoleDTO
from ...models.user_building_role import UserBuildingRole
from ...types import Response


def _get_kwargs(
    building_id: int,
    user_id: int,
    *,
    body: UpdateBuildingRoleDTO,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/v1.0/buildings/{building_id}/roles/{user_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | UserBuildingRole | None:
    if response.status_code == 200:
        response_200 = UserBuildingRole.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403
    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | UserBuildingRole]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    building_id: int,
    user_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateBuildingRoleDTO,
) -> Response[ErrorResponse | UserBuildingRole]:
    """Update Building Role

     Update building role.

    Args:
        building_id (int):
        user_id (int):
        body (UpdateBuildingRoleDTO): Update building role DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, UserBuildingRole]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    building_id: int,
    user_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateBuildingRoleDTO,
) -> ErrorResponse | UserBuildingRole | None:
    """Update Building Role

     Update building role.

    Args:
        building_id (int):
        user_id (int):
        body (UpdateBuildingRoleDTO): Update building role DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, UserBuildingRole]
    """

    return sync_detailed(
        building_id=building_id,
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    building_id: int,
    user_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateBuildingRoleDTO,
) -> Response[ErrorResponse | UserBuildingRole]:
    """Update Building Role

     Update building role.

    Args:
        building_id (int):
        user_id (int):
        body (UpdateBuildingRoleDTO): Update building role DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, UserBuildingRole]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    building_id: int,
    user_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateBuildingRoleDTO,
) -> ErrorResponse | UserBuildingRole | None:
    """Update Building Role

     Update building role.

    Args:
        building_id (int):
        user_id (int):
        body (UpdateBuildingRoleDTO): Update building role DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, UserBuildingRole]
    """

    return (
        await asyncio_detailed(
            building_id=building_id,
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed

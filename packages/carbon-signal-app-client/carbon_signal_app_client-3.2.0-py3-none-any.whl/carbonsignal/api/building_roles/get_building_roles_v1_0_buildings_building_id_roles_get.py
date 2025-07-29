from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.user_building_role import UserBuildingRole
from ...types import Response


def _get_kwargs(
    building_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1.0/buildings/{building_id}/roles",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list["UserBuildingRole"] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UserBuildingRole.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[ErrorResponse | list["UserBuildingRole"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | list["UserBuildingRole"]]:
    """Get Building Roles

     Get building by id.

    Args:
        building_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['UserBuildingRole']]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | list["UserBuildingRole"] | None:
    """Get Building Roles

     Get building by id.

    Args:
        building_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['UserBuildingRole']]
    """

    return sync_detailed(
        building_id=building_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | list["UserBuildingRole"]]:
    """Get Building Roles

     Get building by id.

    Args:
        building_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['UserBuildingRole']]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | list["UserBuildingRole"] | None:
    """Get Building Roles

     Get building by id.

    Args:
        building_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['UserBuildingRole']]
    """

    return (
        await asyncio_detailed(
            building_id=building_id,
            client=client,
        )
    ).parsed

from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.update_team_role_dto import UpdateTeamRoleDTO
from ...models.user_team_role import UserTeamRole
from ...types import Response


def _get_kwargs(
    team_id: int,
    user_id: int,
    *,
    body: UpdateTeamRoleDTO,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/v1.0/teams/{team_id}/roles/{user_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | UserTeamRole | None:
    if response.status_code == 200:
        response_200 = UserTeamRole.from_dict(response.json())

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
) -> Response[ErrorResponse | UserTeamRole]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    user_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateTeamRoleDTO,
) -> Response[ErrorResponse | UserTeamRole]:
    """Update Team Role

     Update team role.

    Args:
        team_id (int):
        user_id (int):
        body (UpdateTeamRoleDTO): Update team role DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, UserTeamRole]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    user_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateTeamRoleDTO,
) -> ErrorResponse | UserTeamRole | None:
    """Update Team Role

     Update team role.

    Args:
        team_id (int):
        user_id (int):
        body (UpdateTeamRoleDTO): Update team role DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, UserTeamRole]
    """

    return sync_detailed(
        team_id=team_id,
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    user_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateTeamRoleDTO,
) -> Response[ErrorResponse | UserTeamRole]:
    """Update Team Role

     Update team role.

    Args:
        team_id (int):
        user_id (int):
        body (UpdateTeamRoleDTO): Update team role DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, UserTeamRole]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    user_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateTeamRoleDTO,
) -> ErrorResponse | UserTeamRole | None:
    """Update Team Role

     Update team role.

    Args:
        team_id (int):
        user_id (int):
        body (UpdateTeamRoleDTO): Update team role DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, UserTeamRole]
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed

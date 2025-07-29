from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.message_response_dto import MessageResponseDTO
from ...models.update_timeline_dto import UpdateTimelineDTO
from ...types import UNSET, Response


def _get_kwargs(
    building_id: int,
    *,
    body: UpdateTimelineDTO,
    team_id: int,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["team_id"] = team_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/v1.0/buildings/{building_id}/timeline",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | MessageResponseDTO | None:
    if response.status_code == 200:
        response_200 = MessageResponseDTO.from_dict(response.json())

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
) -> Response[ErrorResponse | MessageResponseDTO]:
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
    body: UpdateTimelineDTO,
    team_id: int,
) -> Response[ErrorResponse | MessageResponseDTO]:
    """Update Timeline

     Update building timeline.

    Args:
        building_id (int):
        team_id (int):
        body (UpdateTimelineDTO): Update timeline DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, MessageResponseDTO]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        body=body,
        team_id=team_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateTimelineDTO,
    team_id: int,
) -> ErrorResponse | MessageResponseDTO | None:
    """Update Timeline

     Update building timeline.

    Args:
        building_id (int):
        team_id (int):
        body (UpdateTimelineDTO): Update timeline DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, MessageResponseDTO]
    """

    return sync_detailed(
        building_id=building_id,
        client=client,
        body=body,
        team_id=team_id,
    ).parsed


async def asyncio_detailed(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateTimelineDTO,
    team_id: int,
) -> Response[ErrorResponse | MessageResponseDTO]:
    """Update Timeline

     Update building timeline.

    Args:
        building_id (int):
        team_id (int):
        body (UpdateTimelineDTO): Update timeline DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, MessageResponseDTO]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        body=body,
        team_id=team_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateTimelineDTO,
    team_id: int,
) -> ErrorResponse | MessageResponseDTO | None:
    """Update Timeline

     Update building timeline.

    Args:
        building_id (int):
        team_id (int):
        body (UpdateTimelineDTO): Update timeline DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, MessageResponseDTO]
    """

    return (
        await asyncio_detailed(
            building_id=building_id,
            client=client,
            body=body,
            team_id=team_id,
        )
    ).parsed

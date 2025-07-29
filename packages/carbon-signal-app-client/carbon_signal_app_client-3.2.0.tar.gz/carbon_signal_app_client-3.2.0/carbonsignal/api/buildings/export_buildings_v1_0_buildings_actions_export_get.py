from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    team_id: int,
    building_ids: None | Unset | list[int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["team_id"] = team_id

    json_building_ids: None | Unset | list[int]
    if isinstance(building_ids, Unset):
        json_building_ids = UNSET
    elif isinstance(building_ids, list):
        json_building_ids = building_ids

    else:
        json_building_ids = building_ids
    params["building_ids"] = json_building_ids

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1.0/buildings/actions/export",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200
    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    team_id: int,
    building_ids: None | Unset | list[int] = UNSET,
) -> Response[Any | ErrorResponse]:
    """Export Buildings

     Export buildings data for a specific team to Excel.

    Returns an Excel spreadsheet with details of all buildings that the current user can access within a
    given team.
    If building_ids is provided as a comma-separated string, only exports those specific buildings.

    Args:
        team_id (int):
        building_ids (Union[None, Unset, list[int]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        building_ids=building_ids,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    team_id: int,
    building_ids: None | Unset | list[int] = UNSET,
) -> Any | ErrorResponse | None:
    """Export Buildings

     Export buildings data for a specific team to Excel.

    Returns an Excel spreadsheet with details of all buildings that the current user can access within a
    given team.
    If building_ids is provided as a comma-separated string, only exports those specific buildings.

    Args:
        team_id (int):
        building_ids (Union[None, Unset, list[int]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        team_id=team_id,
        building_ids=building_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    team_id: int,
    building_ids: None | Unset | list[int] = UNSET,
) -> Response[Any | ErrorResponse]:
    """Export Buildings

     Export buildings data for a specific team to Excel.

    Returns an Excel spreadsheet with details of all buildings that the current user can access within a
    given team.
    If building_ids is provided as a comma-separated string, only exports those specific buildings.

    Args:
        team_id (int):
        building_ids (Union[None, Unset, list[int]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        building_ids=building_ids,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    team_id: int,
    building_ids: None | Unset | list[int] = UNSET,
) -> Any | ErrorResponse | None:
    """Export Buildings

     Export buildings data for a specific team to Excel.

    Returns an Excel spreadsheet with details of all buildings that the current user can access within a
    given team.
    If building_ids is provided as a comma-separated string, only exports those specific buildings.

    Args:
        team_id (int):
        building_ids (Union[None, Unset, list[int]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            team_id=team_id,
            building_ids=building_ids,
        )
    ).parsed

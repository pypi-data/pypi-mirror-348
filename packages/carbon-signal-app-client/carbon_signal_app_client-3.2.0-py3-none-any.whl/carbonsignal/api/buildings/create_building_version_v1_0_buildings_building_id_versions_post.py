from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.building import Building
from ...models.create_building_version_dto import CreateBuildingVersionDTO
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    building_id: int,
    *,
    body: CreateBuildingVersionDTO,
    team_id: int,
    trigger_baseline: Unset | bool = False,
    trigger_interventions: Unset | bool = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["team_id"] = team_id

    params["trigger_baseline"] = trigger_baseline

    params["trigger_interventions"] = trigger_interventions

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/v1.0/buildings/{building_id}/versions",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Building | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = Building.from_dict(response.json())

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


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Building | ErrorResponse]:
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
    body: CreateBuildingVersionDTO,
    team_id: int,
    trigger_baseline: Unset | bool = False,
    trigger_interventions: Unset | bool = False,
) -> Response[Building | ErrorResponse]:
    """Create Building Version

     Update an existing building.

    This endpoint deals with updating a building with the new data that will require generating a new
    building baseline and intervention analysis.
    This endpoint is distinct from `PUT /v1.0/building/{building_id}` because by updating this set of
    building data, you will require a new
    baseline to be generated, and a new set of interventions to be analyzed. To update building
    attributes that do not require a new baseline,
    see the `PUT /v1.0/building/{building_id}` endpoint.

    Args:
        building_id (int):
        team_id (int):
        trigger_baseline (Union[Unset, bool]): Generate the baseline. Default: False.
        trigger_interventions (Union[Unset, bool]): Start the interventions analysis. Must be
            False unless trigger_baseline is True. Default: False.
        body (CreateBuildingVersionDTO): CreateBuildingVersionDTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Building, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        body=body,
        team_id=team_id,
        trigger_baseline=trigger_baseline,
        trigger_interventions=trigger_interventions,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CreateBuildingVersionDTO,
    team_id: int,
    trigger_baseline: Unset | bool = False,
    trigger_interventions: Unset | bool = False,
) -> Building | ErrorResponse | None:
    """Create Building Version

     Update an existing building.

    This endpoint deals with updating a building with the new data that will require generating a new
    building baseline and intervention analysis.
    This endpoint is distinct from `PUT /v1.0/building/{building_id}` because by updating this set of
    building data, you will require a new
    baseline to be generated, and a new set of interventions to be analyzed. To update building
    attributes that do not require a new baseline,
    see the `PUT /v1.0/building/{building_id}` endpoint.

    Args:
        building_id (int):
        team_id (int):
        trigger_baseline (Union[Unset, bool]): Generate the baseline. Default: False.
        trigger_interventions (Union[Unset, bool]): Start the interventions analysis. Must be
            False unless trigger_baseline is True. Default: False.
        body (CreateBuildingVersionDTO): CreateBuildingVersionDTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Building, ErrorResponse]
    """

    return sync_detailed(
        building_id=building_id,
        client=client,
        body=body,
        team_id=team_id,
        trigger_baseline=trigger_baseline,
        trigger_interventions=trigger_interventions,
    ).parsed


async def asyncio_detailed(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CreateBuildingVersionDTO,
    team_id: int,
    trigger_baseline: Unset | bool = False,
    trigger_interventions: Unset | bool = False,
) -> Response[Building | ErrorResponse]:
    """Create Building Version

     Update an existing building.

    This endpoint deals with updating a building with the new data that will require generating a new
    building baseline and intervention analysis.
    This endpoint is distinct from `PUT /v1.0/building/{building_id}` because by updating this set of
    building data, you will require a new
    baseline to be generated, and a new set of interventions to be analyzed. To update building
    attributes that do not require a new baseline,
    see the `PUT /v1.0/building/{building_id}` endpoint.

    Args:
        building_id (int):
        team_id (int):
        trigger_baseline (Union[Unset, bool]): Generate the baseline. Default: False.
        trigger_interventions (Union[Unset, bool]): Start the interventions analysis. Must be
            False unless trigger_baseline is True. Default: False.
        body (CreateBuildingVersionDTO): CreateBuildingVersionDTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Building, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        body=body,
        team_id=team_id,
        trigger_baseline=trigger_baseline,
        trigger_interventions=trigger_interventions,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CreateBuildingVersionDTO,
    team_id: int,
    trigger_baseline: Unset | bool = False,
    trigger_interventions: Unset | bool = False,
) -> Building | ErrorResponse | None:
    """Create Building Version

     Update an existing building.

    This endpoint deals with updating a building with the new data that will require generating a new
    building baseline and intervention analysis.
    This endpoint is distinct from `PUT /v1.0/building/{building_id}` because by updating this set of
    building data, you will require a new
    baseline to be generated, and a new set of interventions to be analyzed. To update building
    attributes that do not require a new baseline,
    see the `PUT /v1.0/building/{building_id}` endpoint.

    Args:
        building_id (int):
        team_id (int):
        trigger_baseline (Union[Unset, bool]): Generate the baseline. Default: False.
        trigger_interventions (Union[Unset, bool]): Start the interventions analysis. Must be
            False unless trigger_baseline is True. Default: False.
        body (CreateBuildingVersionDTO): CreateBuildingVersionDTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Building, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            building_id=building_id,
            client=client,
            body=body,
            team_id=team_id,
            trigger_baseline=trigger_baseline,
            trigger_interventions=trigger_interventions,
        )
    ).parsed

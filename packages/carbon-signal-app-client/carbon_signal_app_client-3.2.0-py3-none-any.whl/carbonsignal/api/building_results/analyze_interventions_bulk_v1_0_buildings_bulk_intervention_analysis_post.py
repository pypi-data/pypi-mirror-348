from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bulk_trigger_buildings_dto import BulkTriggerBuildingsDTO
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: BulkTriggerBuildingsDTO,
    team_id: int,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["team_id"] = team_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1.0/buildings/bulk-intervention-analysis",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = response.json()
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
    body: BulkTriggerBuildingsDTO,
    team_id: int,
) -> Response[Any | ErrorResponse]:
    """Analyze Interventions Bulk

     Start the intervention analysis for the selected building.

    This endpoint requires that the baseline has already been generated successfully.
    To check the status of the baseline, use the `GET /buildings/{building_id}/results` endpoint.
    To generate a baseline, use the `POST /buildings/{building_id}/baseline` endpoint.

    Once you've successfully started the intervention analysis, you can check the status
    at the same `GET /buildings/{building_id}/results` endpoint.

    Args:
        team_id (int):
        body (BulkTriggerBuildingsDTO): Bulk trigger interventions DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        team_id=team_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: BulkTriggerBuildingsDTO,
    team_id: int,
) -> Any | ErrorResponse | None:
    """Analyze Interventions Bulk

     Start the intervention analysis for the selected building.

    This endpoint requires that the baseline has already been generated successfully.
    To check the status of the baseline, use the `GET /buildings/{building_id}/results` endpoint.
    To generate a baseline, use the `POST /buildings/{building_id}/baseline` endpoint.

    Once you've successfully started the intervention analysis, you can check the status
    at the same `GET /buildings/{building_id}/results` endpoint.

    Args:
        team_id (int):
        body (BulkTriggerBuildingsDTO): Bulk trigger interventions DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
        team_id=team_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BulkTriggerBuildingsDTO,
    team_id: int,
) -> Response[Any | ErrorResponse]:
    """Analyze Interventions Bulk

     Start the intervention analysis for the selected building.

    This endpoint requires that the baseline has already been generated successfully.
    To check the status of the baseline, use the `GET /buildings/{building_id}/results` endpoint.
    To generate a baseline, use the `POST /buildings/{building_id}/baseline` endpoint.

    Once you've successfully started the intervention analysis, you can check the status
    at the same `GET /buildings/{building_id}/results` endpoint.

    Args:
        team_id (int):
        body (BulkTriggerBuildingsDTO): Bulk trigger interventions DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        team_id=team_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: BulkTriggerBuildingsDTO,
    team_id: int,
) -> Any | ErrorResponse | None:
    """Analyze Interventions Bulk

     Start the intervention analysis for the selected building.

    This endpoint requires that the baseline has already been generated successfully.
    To check the status of the baseline, use the `GET /buildings/{building_id}/results` endpoint.
    To generate a baseline, use the `POST /buildings/{building_id}/baseline` endpoint.

    Once you've successfully started the intervention analysis, you can check the status
    at the same `GET /buildings/{building_id}/results` endpoint.

    Args:
        team_id (int):
        body (BulkTriggerBuildingsDTO): Bulk trigger interventions DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            team_id=team_id,
        )
    ).parsed

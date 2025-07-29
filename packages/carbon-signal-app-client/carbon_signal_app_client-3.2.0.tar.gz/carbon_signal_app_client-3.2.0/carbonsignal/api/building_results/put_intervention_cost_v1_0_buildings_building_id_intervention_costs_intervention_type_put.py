from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.custom_update_intervention_cost_dto import CustomUpdateInterventionCostDTO
from ...models.default_update_intervention_cost_dto import DefaultUpdateInterventionCostDTO
from ...models.error_response import ErrorResponse
from ...models.message_response_dto import MessageResponseDTO
from ...models.put_intervention_cost_v10_buildings_building_id_intervention_costs_intervention_type_put_intervention_type import (
    PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionTypePutInterventionType,
)
from ...types import Response


def _get_kwargs(
    building_id: int,
    intervention_type: PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionTypePutInterventionType,
    *,
    body: Union["CustomUpdateInterventionCostDTO", "DefaultUpdateInterventionCostDTO"],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/v1.0/buildings/{building_id}/intervention-costs/{intervention_type}",
    }

    _body: dict[str, Any]
    _body = body.to_dict() if isinstance(body, CustomUpdateInterventionCostDTO) else body.to_dict()

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
    intervention_type: PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionTypePutInterventionType,
    *,
    client: AuthenticatedClient | Client,
    body: Union["CustomUpdateInterventionCostDTO", "DefaultUpdateInterventionCostDTO"],
) -> Response[ErrorResponse | MessageResponseDTO]:
    """Put Intervention Cost

     Update intervention cost.

    Args:
        building_id (int):
        intervention_type (PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionT
            ypePutInterventionType):
        body (Union['CustomUpdateInterventionCostDTO', 'DefaultUpdateInterventionCostDTO']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, MessageResponseDTO]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        intervention_type=intervention_type,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    building_id: int,
    intervention_type: PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionTypePutInterventionType,
    *,
    client: AuthenticatedClient | Client,
    body: Union["CustomUpdateInterventionCostDTO", "DefaultUpdateInterventionCostDTO"],
) -> ErrorResponse | MessageResponseDTO | None:
    """Put Intervention Cost

     Update intervention cost.

    Args:
        building_id (int):
        intervention_type (PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionT
            ypePutInterventionType):
        body (Union['CustomUpdateInterventionCostDTO', 'DefaultUpdateInterventionCostDTO']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, MessageResponseDTO]
    """

    return sync_detailed(
        building_id=building_id,
        intervention_type=intervention_type,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    building_id: int,
    intervention_type: PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionTypePutInterventionType,
    *,
    client: AuthenticatedClient | Client,
    body: Union["CustomUpdateInterventionCostDTO", "DefaultUpdateInterventionCostDTO"],
) -> Response[ErrorResponse | MessageResponseDTO]:
    """Put Intervention Cost

     Update intervention cost.

    Args:
        building_id (int):
        intervention_type (PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionT
            ypePutInterventionType):
        body (Union['CustomUpdateInterventionCostDTO', 'DefaultUpdateInterventionCostDTO']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, MessageResponseDTO]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        intervention_type=intervention_type,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    building_id: int,
    intervention_type: PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionTypePutInterventionType,
    *,
    client: AuthenticatedClient | Client,
    body: Union["CustomUpdateInterventionCostDTO", "DefaultUpdateInterventionCostDTO"],
) -> ErrorResponse | MessageResponseDTO | None:
    """Put Intervention Cost

     Update intervention cost.

    Args:
        building_id (int):
        intervention_type (PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionT
            ypePutInterventionType):
        body (Union['CustomUpdateInterventionCostDTO', 'DefaultUpdateInterventionCostDTO']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, MessageResponseDTO]
    """

    return (
        await asyncio_detailed(
            building_id=building_id,
            intervention_type=intervention_type,
            client=client,
            body=body,
        )
    ).parsed

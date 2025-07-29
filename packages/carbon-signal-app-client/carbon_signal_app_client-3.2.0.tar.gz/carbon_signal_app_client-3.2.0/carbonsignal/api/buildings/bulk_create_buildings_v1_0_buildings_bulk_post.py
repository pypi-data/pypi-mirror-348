from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.building import Building
from ...models.bulk_create_building_dto import BulkCreateBuildingDTO
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: BulkCreateBuildingDTO,
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
        "url": "/v1.0/buildings/bulk",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list["Building"] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Building.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[ErrorResponse | list["Building"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BulkCreateBuildingDTO,
    team_id: int,
    trigger_baseline: Unset | bool = False,
    trigger_interventions: Unset | bool = False,
) -> Response[ErrorResponse | list["Building"]]:
    """Bulk Create Buildings

     Bulk create buildings.

    Args:
        team_id (int):
        trigger_baseline (Union[Unset, bool]): Generate the baseline. Default: False.
        trigger_interventions (Union[Unset, bool]): Start the interventions analysis. Must be
            False unless trigger_baseline is True. Default: False.
        body (BulkCreateBuildingDTO): Bulk create building DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['Building']]]
    """

    kwargs = _get_kwargs(
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
    *,
    client: AuthenticatedClient | Client,
    body: BulkCreateBuildingDTO,
    team_id: int,
    trigger_baseline: Unset | bool = False,
    trigger_interventions: Unset | bool = False,
) -> ErrorResponse | list["Building"] | None:
    """Bulk Create Buildings

     Bulk create buildings.

    Args:
        team_id (int):
        trigger_baseline (Union[Unset, bool]): Generate the baseline. Default: False.
        trigger_interventions (Union[Unset, bool]): Start the interventions analysis. Must be
            False unless trigger_baseline is True. Default: False.
        body (BulkCreateBuildingDTO): Bulk create building DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['Building']]
    """

    return sync_detailed(
        client=client,
        body=body,
        team_id=team_id,
        trigger_baseline=trigger_baseline,
        trigger_interventions=trigger_interventions,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BulkCreateBuildingDTO,
    team_id: int,
    trigger_baseline: Unset | bool = False,
    trigger_interventions: Unset | bool = False,
) -> Response[ErrorResponse | list["Building"]]:
    """Bulk Create Buildings

     Bulk create buildings.

    Args:
        team_id (int):
        trigger_baseline (Union[Unset, bool]): Generate the baseline. Default: False.
        trigger_interventions (Union[Unset, bool]): Start the interventions analysis. Must be
            False unless trigger_baseline is True. Default: False.
        body (BulkCreateBuildingDTO): Bulk create building DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['Building']]]
    """

    kwargs = _get_kwargs(
        body=body,
        team_id=team_id,
        trigger_baseline=trigger_baseline,
        trigger_interventions=trigger_interventions,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: BulkCreateBuildingDTO,
    team_id: int,
    trigger_baseline: Unset | bool = False,
    trigger_interventions: Unset | bool = False,
) -> ErrorResponse | list["Building"] | None:
    """Bulk Create Buildings

     Bulk create buildings.

    Args:
        team_id (int):
        trigger_baseline (Union[Unset, bool]): Generate the baseline. Default: False.
        trigger_interventions (Union[Unset, bool]): Start the interventions analysis. Must be
            False unless trigger_baseline is True. Default: False.
        body (BulkCreateBuildingDTO): Bulk create building DTO.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['Building']]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            team_id=team_id,
            trigger_baseline=trigger_baseline,
            trigger_interventions=trigger_interventions,
        )
    ).parsed

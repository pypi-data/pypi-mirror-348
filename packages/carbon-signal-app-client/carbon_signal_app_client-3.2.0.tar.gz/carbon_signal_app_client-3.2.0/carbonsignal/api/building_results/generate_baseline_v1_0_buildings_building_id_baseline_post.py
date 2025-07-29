from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response


def _get_kwargs(
    building_id: int,
    *,
    team_id: int,
    trigger_interventions: bool,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["team_id"] = team_id

    params["trigger_interventions"] = trigger_interventions

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/v1.0/buildings/{building_id}/baseline",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200
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
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
    team_id: int,
    trigger_interventions: bool,
) -> Response[Any | ErrorResponse]:
    """Generate Baseline

     Generate the selected building's baseline.

    To check the status of the baseline, use the `GET /buildings/{building_id}/results` endpoint.

    Args:
        building_id (int):
        team_id (int):
        trigger_interventions (bool): Also trigger the interventions analysis?

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        team_id=team_id,
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
    team_id: int,
    trigger_interventions: bool,
) -> Any | ErrorResponse | None:
    """Generate Baseline

     Generate the selected building's baseline.

    To check the status of the baseline, use the `GET /buildings/{building_id}/results` endpoint.

    Args:
        building_id (int):
        team_id (int):
        trigger_interventions (bool): Also trigger the interventions analysis?

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        building_id=building_id,
        client=client,
        team_id=team_id,
        trigger_interventions=trigger_interventions,
    ).parsed


async def asyncio_detailed(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
    team_id: int,
    trigger_interventions: bool,
) -> Response[Any | ErrorResponse]:
    """Generate Baseline

     Generate the selected building's baseline.

    To check the status of the baseline, use the `GET /buildings/{building_id}/results` endpoint.

    Args:
        building_id (int):
        team_id (int):
        trigger_interventions (bool): Also trigger the interventions analysis?

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        team_id=team_id,
        trigger_interventions=trigger_interventions,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
    team_id: int,
    trigger_interventions: bool,
) -> Any | ErrorResponse | None:
    """Generate Baseline

     Generate the selected building's baseline.

    To check the status of the baseline, use the `GET /buildings/{building_id}/results` endpoint.

    Args:
        building_id (int):
        team_id (int):
        trigger_interventions (bool): Also trigger the interventions analysis?

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            building_id=building_id,
            client=client,
            team_id=team_id,
            trigger_interventions=trigger_interventions,
        )
    ).parsed

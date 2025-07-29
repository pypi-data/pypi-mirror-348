from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.building import Building
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    building_id: int,
    version_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/v1.0/buildings/{building_id}/versions/{version_id}/restore",
    }

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
    version_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Building | ErrorResponse]:
    """Restore Building Version

     Restore a building version.

    Args:
        building_id (int):
        version_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Building, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        version_id=version_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    building_id: int,
    version_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Building | ErrorResponse | None:
    """Restore Building Version

     Restore a building version.

    Args:
        building_id (int):
        version_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Building, ErrorResponse]
    """

    return sync_detailed(
        building_id=building_id,
        version_id=version_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    building_id: int,
    version_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Building | ErrorResponse]:
    """Restore Building Version

     Restore a building version.

    Args:
        building_id (int):
        version_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Building, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        version_id=version_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    building_id: int,
    version_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Building | ErrorResponse | None:
    """Restore Building Version

     Restore a building version.

    Args:
        building_id (int):
        version_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Building, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            building_id=building_id,
            version_id=version_id,
            client=client,
        )
    ).parsed

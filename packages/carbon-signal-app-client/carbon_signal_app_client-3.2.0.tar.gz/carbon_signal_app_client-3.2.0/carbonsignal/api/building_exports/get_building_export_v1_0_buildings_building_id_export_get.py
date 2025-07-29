from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    building_id: int,
    *,
    include_diagnostic: Unset | bool = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["include_diagnostic"] = include_diagnostic

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1.0/buildings/{building_id}/export",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = cast(Any, None)
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
    include_diagnostic: Unset | bool = False,
) -> Response[Any | ErrorResponse]:
    """Get Building Export

     Export building data to an XLSX spreadsheet.

    Args:
        building_id (int):
        include_diagnostic (Union[Unset, bool]): Include diagnostic data Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        include_diagnostic=include_diagnostic,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
    include_diagnostic: Unset | bool = False,
) -> Any | ErrorResponse | None:
    """Get Building Export

     Export building data to an XLSX spreadsheet.

    Args:
        building_id (int):
        include_diagnostic (Union[Unset, bool]): Include diagnostic data Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        building_id=building_id,
        client=client,
        include_diagnostic=include_diagnostic,
    ).parsed


async def asyncio_detailed(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
    include_diagnostic: Unset | bool = False,
) -> Response[Any | ErrorResponse]:
    """Get Building Export

     Export building data to an XLSX spreadsheet.

    Args:
        building_id (int):
        include_diagnostic (Union[Unset, bool]): Include diagnostic data Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
        include_diagnostic=include_diagnostic,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
    include_diagnostic: Unset | bool = False,
) -> Any | ErrorResponse | None:
    """Get Building Export

     Export building data to an XLSX spreadsheet.

    Args:
        building_id (int):
        include_diagnostic (Union[Unset, bool]): Include diagnostic data Default: False.

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
            include_diagnostic=include_diagnostic,
        )
    ).parsed

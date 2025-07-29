from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    provider_id: int,
    *,
    return_to: None | Unset | str = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_return_to: None | Unset | str
    json_return_to = UNSET if isinstance(return_to, Unset) else return_to
    params["return_to"] = json_return_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1.0/auth/sso/{provider_id}/login",
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
    provider_id: int,
    *,
    client: AuthenticatedClient | Client,
    return_to: None | Unset | str = UNSET,
) -> Response[Any | ErrorResponse]:
    """Sso Redirect

     Initialize SSO login flow.

    This method returns a 302 redirect to the requested SSO provider's login page.

    Args:
        provider_id (int):
        return_to (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        provider_id=provider_id,
        return_to=return_to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    provider_id: int,
    *,
    client: AuthenticatedClient | Client,
    return_to: None | Unset | str = UNSET,
) -> Any | ErrorResponse | None:
    """Sso Redirect

     Initialize SSO login flow.

    This method returns a 302 redirect to the requested SSO provider's login page.

    Args:
        provider_id (int):
        return_to (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        provider_id=provider_id,
        client=client,
        return_to=return_to,
    ).parsed


async def asyncio_detailed(
    provider_id: int,
    *,
    client: AuthenticatedClient | Client,
    return_to: None | Unset | str = UNSET,
) -> Response[Any | ErrorResponse]:
    """Sso Redirect

     Initialize SSO login flow.

    This method returns a 302 redirect to the requested SSO provider's login page.

    Args:
        provider_id (int):
        return_to (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        provider_id=provider_id,
        return_to=return_to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    provider_id: int,
    *,
    client: AuthenticatedClient | Client,
    return_to: None | Unset | str = UNSET,
) -> Any | ErrorResponse | None:
    """Sso Redirect

     Initialize SSO login flow.

    This method returns a 302 redirect to the requested SSO provider's login page.

    Args:
        provider_id (int):
        return_to (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            provider_id=provider_id,
            client=client,
            return_to=return_to,
        )
    ).parsed

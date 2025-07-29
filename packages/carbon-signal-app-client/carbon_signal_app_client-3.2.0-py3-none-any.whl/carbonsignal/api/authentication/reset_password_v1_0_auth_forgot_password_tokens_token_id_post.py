from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.update_password_dto import UpdatePasswordDTO
from ...models.user_with_settings import UserWithSettings
from ...types import Response


def _get_kwargs(
    token_id: str,
    *,
    body: UpdatePasswordDTO,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/v1.0/auth/forgot-password/tokens/{token_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | UserWithSettings | None:
    if response.status_code == 200:
        response_200 = UserWithSettings.from_dict(response.json())

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
) -> Response[ErrorResponse | UserWithSettings]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    token_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdatePasswordDTO,
) -> Response[ErrorResponse | UserWithSettings]:
    """Reset Password

     Update a user's password and log them in.

    Args:
        token_id (str):
        body (UpdatePasswordDTO): POST model for updating password.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, UserWithSettings]]
    """

    kwargs = _get_kwargs(
        token_id=token_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    token_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdatePasswordDTO,
) -> ErrorResponse | UserWithSettings | None:
    """Reset Password

     Update a user's password and log them in.

    Args:
        token_id (str):
        body (UpdatePasswordDTO): POST model for updating password.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, UserWithSettings]
    """

    return sync_detailed(
        token_id=token_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    token_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdatePasswordDTO,
) -> Response[ErrorResponse | UserWithSettings]:
    """Reset Password

     Update a user's password and log them in.

    Args:
        token_id (str):
        body (UpdatePasswordDTO): POST model for updating password.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, UserWithSettings]]
    """

    kwargs = _get_kwargs(
        token_id=token_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    token_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdatePasswordDTO,
) -> ErrorResponse | UserWithSettings | None:
    """Reset Password

     Update a user's password and log them in.

    Args:
        token_id (str):
        body (UpdatePasswordDTO): POST model for updating password.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, UserWithSettings]
    """

    return (
        await asyncio_detailed(
            token_id=token_id,
            client=client,
            body=body,
        )
    ).parsed

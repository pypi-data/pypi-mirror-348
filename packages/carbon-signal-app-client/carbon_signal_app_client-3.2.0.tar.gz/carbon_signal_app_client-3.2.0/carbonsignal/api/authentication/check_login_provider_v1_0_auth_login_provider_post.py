from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.auth_provider_check_dto import AuthProviderCheckDTO
from ...models.auth_provider_password import AuthProviderPassword
from ...models.auth_provider_sso import AuthProviderSSO
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    body: AuthProviderCheckDTO,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1.0/auth/login-provider",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Union["AuthProviderPassword", "AuthProviderSSO"] | None:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union["AuthProviderPassword", "AuthProviderSSO"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = AuthProviderPassword.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = AuthProviderSSO.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

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
) -> Response[ErrorResponse | Union["AuthProviderPassword", "AuthProviderSSO"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AuthProviderCheckDTO,
) -> Response[ErrorResponse | Union["AuthProviderPassword", "AuthProviderSSO"]]:
    """Check Login Provider

     Get the login provider for a user.

    Args:
        body (AuthProviderCheckDTO): Request model for SSO status check.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, Union['AuthProviderPassword', 'AuthProviderSSO']]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: AuthProviderCheckDTO,
) -> ErrorResponse | Union["AuthProviderPassword", "AuthProviderSSO"] | None:
    """Check Login Provider

     Get the login provider for a user.

    Args:
        body (AuthProviderCheckDTO): Request model for SSO status check.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, Union['AuthProviderPassword', 'AuthProviderSSO']]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AuthProviderCheckDTO,
) -> Response[ErrorResponse | Union["AuthProviderPassword", "AuthProviderSSO"]]:
    """Check Login Provider

     Get the login provider for a user.

    Args:
        body (AuthProviderCheckDTO): Request model for SSO status check.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, Union['AuthProviderPassword', 'AuthProviderSSO']]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: AuthProviderCheckDTO,
) -> ErrorResponse | Union["AuthProviderPassword", "AuthProviderSSO"] | None:
    """Check Login Provider

     Get the login provider for a user.

    Args:
        body (AuthProviderCheckDTO): Request model for SSO status check.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, Union['AuthProviderPassword', 'AuthProviderSSO']]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.avatar import Avatar
from ...models.body_post_avatar_v10_uploads_avatars_post import BodyPostAvatarV10UploadsAvatarsPost
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    body: BodyPostAvatarV10UploadsAvatarsPost,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1.0/uploads/avatars",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Avatar | ErrorResponse | None:
    if response.status_code == 201:
        response_201 = Avatar.from_dict(response.json())

        return response_201
    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401
    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Avatar | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BodyPostAvatarV10UploadsAvatarsPost,
) -> Response[Avatar | ErrorResponse]:
    """Post Avatar

     Upload a new avatar.

    Returns the avatar id and url, which can then be posted to the PUT /users/{user_id} route to update
    the user's avatar.

    The user is expected to send FormData with the keyed by the name: `file`.
    This file must be no greater than 1MB and must have a content type of: `image/jpeg`, `image/png`,
    `image/gif`, or `image/webp`.

    Args:
        body (BodyPostAvatarV10UploadsAvatarsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Avatar, ErrorResponse]]
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
    body: BodyPostAvatarV10UploadsAvatarsPost,
) -> Avatar | ErrorResponse | None:
    """Post Avatar

     Upload a new avatar.

    Returns the avatar id and url, which can then be posted to the PUT /users/{user_id} route to update
    the user's avatar.

    The user is expected to send FormData with the keyed by the name: `file`.
    This file must be no greater than 1MB and must have a content type of: `image/jpeg`, `image/png`,
    `image/gif`, or `image/webp`.

    Args:
        body (BodyPostAvatarV10UploadsAvatarsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Avatar, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BodyPostAvatarV10UploadsAvatarsPost,
) -> Response[Avatar | ErrorResponse]:
    """Post Avatar

     Upload a new avatar.

    Returns the avatar id and url, which can then be posted to the PUT /users/{user_id} route to update
    the user's avatar.

    The user is expected to send FormData with the keyed by the name: `file`.
    This file must be no greater than 1MB and must have a content type of: `image/jpeg`, `image/png`,
    `image/gif`, or `image/webp`.

    Args:
        body (BodyPostAvatarV10UploadsAvatarsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Avatar, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: BodyPostAvatarV10UploadsAvatarsPost,
) -> Avatar | ErrorResponse | None:
    """Post Avatar

     Upload a new avatar.

    Returns the avatar id and url, which can then be posted to the PUT /users/{user_id} route to update
    the user's avatar.

    The user is expected to send FormData with the keyed by the name: `file`.
    This file must be no greater than 1MB and must have a content type of: `image/jpeg`, `image/png`,
    `image/gif`, or `image/webp`.

    Args:
        body (BodyPostAvatarV10UploadsAvatarsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Avatar, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

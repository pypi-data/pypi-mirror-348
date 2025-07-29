from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_upload_file_v10_buildings_uploads_post import BodyUploadFileV10BuildingsUploadsPost
from ...models.error_response import ErrorResponse
from ...models.inspected_building import InspectedBuilding
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: BodyUploadFileV10BuildingsUploadsPost,
    team_id: int,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["team_id"] = team_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1.0/buildings/uploads",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list["InspectedBuilding"] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = InspectedBuilding.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[ErrorResponse | list["InspectedBuilding"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BodyUploadFileV10BuildingsUploadsPost,
    team_id: int,
) -> Response[ErrorResponse | list["InspectedBuilding"]]:
    """Upload File

     Process excel file for building entities to be added.

    Input an excel file that follows the excel template and get back building entities
    that can be published to the create building endpoints in a later step. This endpoint
    will also return warnings and errors that were found in the buildings represented in
    the excel file.

    Args:
        team_id (int):
        body (BodyUploadFileV10BuildingsUploadsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['InspectedBuilding']]]
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
    body: BodyUploadFileV10BuildingsUploadsPost,
    team_id: int,
) -> ErrorResponse | list["InspectedBuilding"] | None:
    """Upload File

     Process excel file for building entities to be added.

    Input an excel file that follows the excel template and get back building entities
    that can be published to the create building endpoints in a later step. This endpoint
    will also return warnings and errors that were found in the buildings represented in
    the excel file.

    Args:
        team_id (int):
        body (BodyUploadFileV10BuildingsUploadsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['InspectedBuilding']]
    """

    return sync_detailed(
        client=client,
        body=body,
        team_id=team_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BodyUploadFileV10BuildingsUploadsPost,
    team_id: int,
) -> Response[ErrorResponse | list["InspectedBuilding"]]:
    """Upload File

     Process excel file for building entities to be added.

    Input an excel file that follows the excel template and get back building entities
    that can be published to the create building endpoints in a later step. This endpoint
    will also return warnings and errors that were found in the buildings represented in
    the excel file.

    Args:
        team_id (int):
        body (BodyUploadFileV10BuildingsUploadsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, list['InspectedBuilding']]]
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
    body: BodyUploadFileV10BuildingsUploadsPost,
    team_id: int,
) -> ErrorResponse | list["InspectedBuilding"] | None:
    """Upload File

     Process excel file for building entities to be added.

    Input an excel file that follows the excel template and get back building entities
    that can be published to the create building endpoints in a later step. This endpoint
    will also return warnings and errors that were found in the buildings represented in
    the excel file.

    Args:
        team_id (int):
        body (BodyUploadFileV10BuildingsUploadsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, list['InspectedBuilding']]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            team_id=team_id,
        )
    ).parsed

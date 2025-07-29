import aiohttp
from typing import Optional

from gestell.types import BaseRequest, BaseResponse
from gestell.types import OrganizationResult


class GetOrganizationRequest(BaseRequest):
    id: str


class GetOrganizationResponse(BaseResponse):
    result: Optional[OrganizationResult] = None


async def get_organization(
    request: GetOrganizationRequest,
) -> GetOrganizationResponse:
    url = f'{request.api_url}/api/organization/{request.id}'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url,
                headers={
                    'Authorization': f'BEARER {request.api_key}',
                    'Content-Type': 'application/json',
                },
            ) as response:
                if not response.ok:
                    error_response = await response.json()
                    if request.debug:
                        print(error_response)
                    return GetOrganizationResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error retrieving the organization'
                        ),
                    )

                response_data = await response.json()
                return GetOrganizationResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return GetOrganizationResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
            )

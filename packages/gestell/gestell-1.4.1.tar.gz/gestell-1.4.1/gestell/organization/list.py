import aiohttp
from typing import List, Optional

from gestell.types import BaseRequest, BaseResponse
from gestell.types import OrganizationListResult


class GetOrganizationsRequest(BaseRequest):
    search: Optional[str]
    take: Optional[int]
    skip: Optional[int]
    extended: Optional[bool]


class GetOrganizationsResponse(BaseResponse):
    result: Optional[List[OrganizationListResult]] = None


async def list_organizations(
    request: GetOrganizationsRequest,
) -> GetOrganizationsResponse:
    url = f'{request.api_url}/api/organization'
    params = {}
    if request.search:
        params['search'] = request.search
    if request.take:
        params['take'] = request.take
    if request.skip:
        params['skip'] = request.skip
    if request.extended:
        params['extended'] = request.extended

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url,
                headers={
                    'Authorization': f'BEARER {request.api_key}',
                    'Content-Type': 'application/json',
                },
                params=params,
            ) as response:
                if not response.ok:
                    error_response = await response.json()
                    if request.debug:
                        print(error_response)
                    return GetOrganizationsResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error retrieving the organizations'
                        ),
                    )

                response_data = await response.json()
                return GetOrganizationsResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return GetOrganizationsResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
            )

import aiohttp
import json
from typing import List, Optional

from gestell.types import BaseRequest, BaseResponse
from gestell.types import OrganizationMemberRequest


class CreateOrganizationRequest(BaseRequest):
    name: str
    description: str
    members: Optional[List[OrganizationMemberRequest]]


class CreateOrganizationResponse(BaseResponse):
    id: str


async def create_organization(
    request: CreateOrganizationRequest,
) -> CreateOrganizationResponse:
    url = f'{request.api_url}/api/organization'

    payload = {
        'name': request.name,
        'description': request.description,
        'members': [member.__dict__ for member in request.members]
        if request.members
        else [],
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(
                url,
                headers={
                    'Authorization': f'BEARER {request.api_key}',
                    'Content-Type': 'application/json',
                },
                data=json.dumps(payload),
            ) as response:
                if not response.ok:
                    error_response = await response.json()
                    if request.debug:
                        print(error_response)
                    return CreateOrganizationResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error creating an organization'
                        ),
                        id='',
                    )

                response_data = await response.json()
                return CreateOrganizationResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return CreateOrganizationResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                id='',
            )

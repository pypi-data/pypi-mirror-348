import json
import aiohttp
from typing import List

from gestell.types import BaseRequest, BaseResponse, OrganizationMemberRequest


class AddMembersRequest(BaseRequest):
    id: str
    members: List[OrganizationMemberRequest]


class AddMembersResponse(BaseResponse):
    pass


async def add_members(request: AddMembersRequest) -> AddMembersResponse:
    url = f'{request.api_url}/api/organization/{request.id}/member'
    payload = {'members': [member.__dict__ for member in request.members]}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
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
                    return AddMembersResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error adding members'
                        ),
                    )

                response_data = await response.json()
                return AddMembersResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return AddMembersResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
            )

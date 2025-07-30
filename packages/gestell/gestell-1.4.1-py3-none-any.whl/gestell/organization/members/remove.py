import aiohttp
from typing import List

from gestell.types import BaseRequest, BaseResponse


class RemoveMembersRequest(BaseRequest):
    id: str
    members: List[str]


class RemoveMembersResponse(BaseResponse):
    pass


async def remove_members(
    request: RemoveMembersRequest,
) -> RemoveMembersResponse:
    url = f'{request.api_url}/api/organization/{request.id}/member'
    params = [('id', member) for member in request.members]

    async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(
                url,
                headers={
                    'Authorization': f'BEARER {request.api_key}',
                },
                params=params,
            ) as response:
                if not response.ok:
                    error_response = await response.json()
                    if request.debug:
                        print(error_response)
                    return RemoveMembersResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error removing members'
                        ),
                    )

                response_data = await response.json()
                return RemoveMembersResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return RemoveMembersResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
            )

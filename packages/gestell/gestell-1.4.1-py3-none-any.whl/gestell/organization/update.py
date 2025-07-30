import aiohttp
import json

from gestell.types import BaseRequest, BaseResponse


class UpdateOrganizationRequest(BaseRequest):
    id: str
    name: str
    description: str


class UpdateOrganizationResponse(BaseResponse):
    pass


async def update_organization(
    request: UpdateOrganizationRequest,
) -> UpdateOrganizationResponse:
    url = f'{request.api_url}/api/organization/{request.id}'
    payload = {
        'name': request.name,
        'description': request.description,
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.patch(
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
                    return UpdateOrganizationResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error updating the organization'
                        ),
                    )

                response_data = await response.json()
                return UpdateOrganizationResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return UpdateOrganizationResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
            )

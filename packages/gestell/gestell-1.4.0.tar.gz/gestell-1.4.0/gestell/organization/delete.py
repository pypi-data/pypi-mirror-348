import aiohttp

from gestell.types import BaseRequest, BaseResponse


class DeleteOrganizationRequest(BaseRequest):
    id: str


async def delete_organization(
    request: DeleteOrganizationRequest,
) -> BaseResponse:
    url = f'{request.api_url}/api/organization/{request.id}'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(
                url,
                headers={
                    'Authorization': f'BEARER {request.api_key}',
                },
            ) as response:
                if not response.ok:
                    error_response = await response.json()
                    if request.debug:
                        print(error_response)
                    return BaseResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error deleting the organization'
                        ),
                    )

                response_data = await response.json()
                return BaseResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return BaseResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
            )

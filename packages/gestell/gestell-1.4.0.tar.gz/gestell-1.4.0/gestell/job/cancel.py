import aiohttp
from typing import List

from gestell.types import BaseRequest, BaseResponse


class CancelJobsRequest(BaseRequest):
    collection_id: str
    ids: List[str]


class CancelJobsResponse(BaseResponse):
    pass


async def cancel_jobs(request: CancelJobsRequest) -> CancelJobsResponse:
    url = f'{request.api_url}/api/collection/{request.collection_id}/job'

    params = [('ids', id) for id in request.ids]

    async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(
                url,
                headers={'Authorization': f'BEARER {request.api_key}'},
                params=params,
            ) as response:
                if not response.ok:
                    error_response = await response.json()
                    if request.debug:
                        print(error_response)
                    return CancelJobsResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error cancelling jobs'
                        ),
                    )

                response_data = await response.json()
                return CancelJobsResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return CancelJobsResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
            )

import aiohttp
from typing import Optional

from gestell.types import BaseRequest, BaseResponse, Job


class GetJobRequest(BaseRequest):
    collection_id: str
    document_id: str


class GetJobResponse(BaseResponse):
    result: Optional[Job]


async def get_job(request: GetJobRequest) -> GetJobResponse:
    url = f'{request.api_url}/api/collection/{request.collection_id}/job/{request.document_id}'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url,
                headers={'Authorization': f'BEARER {request.api_key}'},
            ) as response:
                if not response.ok:
                    error_response = await response.json()
                    if request.debug:
                        print(error_response)
                    return GetJobResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error retrieving the job'
                        ),
                        result=None,
                    )

                response_data = await response.json()
                return GetJobResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return GetJobResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                result=None,
            )

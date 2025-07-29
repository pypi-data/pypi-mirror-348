import aiohttp
import json
from typing import List

from gestell.types import BaseRequest, BaseResponse, JobType


class ReprocessDocumentsRequest(BaseRequest):
    collection_id: str
    ids: List[str]
    type: JobType


class ReprocessDocumentsResponse(BaseResponse):
    pass


async def reprocess_document(
    request: ReprocessDocumentsRequest,
) -> ReprocessDocumentsResponse:
    url = f'{request.api_url}/api/collection/{request.collection_id}/job'
    payload = {
        'ids': request.ids,
        'type': request.type,
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
                    return ReprocessDocumentsResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error reprocessing jobs'
                        ),
                    )

                response_data = await response.json()
                return ReprocessDocumentsResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return ReprocessDocumentsResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
            )

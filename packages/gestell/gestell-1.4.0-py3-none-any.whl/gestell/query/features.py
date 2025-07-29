import aiohttp
import json
from typing import List, Optional

from gestell.types import BaseRequest, BaseResponse


class FeaturesQueryRequest(BaseRequest):
    collection_id: str
    category_id: str
    skip: Optional[int] = 0
    take: Optional[int] = 10


class FeaturesQueryResponse(BaseResponse):
    result: List[dict]


async def featuresQuery(
    request: FeaturesQueryRequest,
) -> FeaturesQueryResponse:
    url = f'{request.api_url}/api/collection/{request.collection_id}/features'

    payload = {
        'collectionId': request.collection_id,
        'categoryId': request.category_id,
        'skip': request.skip,
        'take': request.take,
    }

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
                    return FeaturesQueryResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error running the features query'
                        ),
                        result=[],
                    )

                response_data = await response.json()
                return FeaturesQueryResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return FeaturesQueryResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                result=[],
            )

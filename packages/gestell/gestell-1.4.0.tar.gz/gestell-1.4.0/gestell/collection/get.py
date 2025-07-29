import aiohttp
from typing import Optional

from gestell.types import BaseRequest, BaseResponse
from gestell.types import Collection, CollectionStats


class GetCollectionRequest(BaseRequest):
    collection_id: str


class GetCollectionResponse(BaseResponse):
    result: Optional[Collection]
    stats: Optional[CollectionStats]


async def get_collection(
    request: GetCollectionRequest,
) -> GetCollectionResponse:
    url = f'{request.api_url}/api/collection/{request.collection_id}'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url,
                headers={
                    'Authorization': f'BEARER {request.api_key}',
                    'Content-Type': 'application/json',
                },
            ) as response:
                if not response.ok:
                    error_response = await response.json()
                    if request.debug:
                        print(error_response)
                    return GetCollectionResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error retrieving the collection'
                        ),
                        result=None,
                        stats=None,
                    )

                response_data = await response.json()
                return GetCollectionResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return GetCollectionResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                result=None,
                stats=None,
            )

import aiohttp
from typing import List, Optional

from gestell.types import BaseRequest, BaseResponse, Collection


class GetCollectionsRequest(BaseRequest):
    search: Optional[str] = None
    take: Optional[int] = None
    skip: Optional[int] = None
    extended: Optional[bool] = None


class GetCollectionsResponse(BaseResponse):
    result: List[Collection]


async def list_collections(
    request: GetCollectionsRequest,
) -> GetCollectionsResponse:
    url = f'{request.api_url}/api/collection'
    params = {}
    if request.search:
        params['search'] = request.search
    if request.take:
        params['take'] = str(request.take)
    if request.skip:
        params['skip'] = str(request.skip)
    if request.extended:
        params['extended'] = str(request.extended)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
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
                    return GetCollectionsResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error retrieving collections'
                        ),
                        result=[],
                    )

                response_data = await response.json()
                return GetCollectionsResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return GetCollectionsResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                result=[],
            )

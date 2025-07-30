import aiohttp

from gestell.types import BaseRequest, BaseResponse


class RemoveCategoryRequest(BaseRequest):
    collection_id: str
    category_id: str


class RemoveCategoryResponse(BaseResponse):
    pass


async def remove_category(
    request: RemoveCategoryRequest,
) -> RemoveCategoryResponse:
    url = f'{request.api_url}/api/collection/{request.collection_id}/category/{request.category_id}'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(
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
                    return RemoveCategoryResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error removing the category'
                        ),
                    )

                response_data = await response.json()
                return RemoveCategoryResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return RemoveCategoryResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
            )

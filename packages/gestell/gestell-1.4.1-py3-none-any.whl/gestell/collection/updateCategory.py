import aiohttp
import json
from typing import Optional

from gestell.types import BaseRequest, BaseResponse, CategoryType


class UpdateCategoryRequest(BaseRequest):
    collection_id: str
    category_id: str
    name: Optional[str] = None
    type: Optional[CategoryType] = None
    instructions: Optional[str] = None
    single_entry: Optional[bool] = None


class UpdateCategoryResponse(BaseResponse):
    pass


async def update_category(
    request: UpdateCategoryRequest,
) -> UpdateCategoryResponse:
    url = f'{request.api_url}/api/collection/{request.collection_id}/category'

    payload = {'categoryId': request.category_id}

    if request.name is not None:
        payload['name'] = request.name
    if request.type is not None:
        payload['type'] = request.type
    if request.instructions is not None:
        payload['instructions'] = request.instructions
    if request.single_entry is not None:
        payload['singleEntry'] = request.single_entry

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
                    return UpdateCategoryResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error updating the category'
                        ),
                    )

                response_data = await response.json()
                return UpdateCategoryResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return UpdateCategoryResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
            )

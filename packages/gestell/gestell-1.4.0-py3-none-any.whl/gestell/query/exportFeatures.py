import aiohttp
from typing import Any, Literal

from gestell.types import BaseRequest


class ExportFeaturesRequest(BaseRequest):
    collection_id: str
    category_id: str
    type: Literal['json', 'csv']


async def export_features(
    request: ExportFeaturesRequest,
) -> Any:
    url = f'{request.api_url}/api/collection/{request.collection_id}/features/export?categoryId={request.category_id}&type={request.type}'

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
                    return 'There was an error retrieving the features'

                response_data = await response.json()
                return response_data
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return f'An error occurred during the request: {e}'

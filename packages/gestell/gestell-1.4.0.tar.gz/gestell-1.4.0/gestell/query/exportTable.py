import aiohttp
from typing import Any, Literal

from gestell.types import BaseRequest


class ExportTableRequest(BaseRequest):
    collection_id: str
    category_id: str
    type: Literal['json', 'csv']


async def export_table(
    request: ExportTableRequest,
) -> Any:
    url = f'{request.api_url}/api/collection/{request.collection_id}/table/export?categoryId={request.category_id}&type={request.type}'

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
                    return 'There was an error retrieving the table'

                response_data = await response.json()
                return response_data
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return f'An error occurred during the request: {e}'

import aiohttp
from typing import Literal, Optional

from gestell.types import BaseRequest


class ExportDocumentRequest(BaseRequest):
    collection_id: str
    document_id: str
    type: Optional[Literal['json', 'csv']] = 'json'


async def export_document(request: ExportDocumentRequest) -> any:
    url = f'{request.api_url}/api/collection/{request.collection_id}/document/{request.document_id}/export?type={request.type}'

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
                    return 'ERROR Retrieving Document'

                if request.type == 'json':
                    response_data = await response.json()
                    return response_data
                else:
                    return await response.text()
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return f'An error occurred during the request: {e}'

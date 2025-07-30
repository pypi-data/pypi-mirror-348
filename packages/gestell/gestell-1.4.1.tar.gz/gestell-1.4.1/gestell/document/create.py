import aiohttp
import json
from typing import Optional

from gestell.types import BaseRequest, BaseResponse


class CreateDocumentRequest(BaseRequest):
    collection_id: str
    name: str
    path: str
    type: str
    instructions: Optional[str] = None
    job: Optional[bool] = None
    tables: Optional[bool] = None


class CreateDocumentResponse(BaseResponse):
    id: str


async def create_document(
    request: CreateDocumentRequest,
) -> CreateDocumentResponse:
    url = f'{request.api_url}/api/collection/{request.collection_id}/document'

    payload = {
        'name': request.name,
        'path': request.path,
        'type': request.type,
        'instructions': request.instructions,
        'job': request.job,
        'tables': request.tables,
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
                    return CreateDocumentResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error creating the document'
                        ),
                        id='',
                    )

                response_data = await response.json()
                return CreateDocumentResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return CreateDocumentResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                id='',
            )

import aiohttp
import json
from typing import Optional

from gestell.types import BaseRequest, BaseResponse


class UpdateDocumentRequest(BaseRequest):
    id: str
    document_id: str
    name: Optional[str] = None
    instructions: Optional[str] = None
    job: Optional[bool] = None
    tables: Optional[bool] = None


async def update_document(
    request: UpdateDocumentRequest,
) -> BaseResponse:
    url = (
        f'{request.api_url}/api/collection/{request.id}/document/{request.document_id}'
    )

    payload = {
        k: v
        for k, v in {
            'name': request.name,
            'instructions': request.instructions,
            'job': request.job,
            'tables': request.tables,
        }.items()
        if v is not None
    }

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
                    return BaseResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error updating the document'
                        ),
                    )

                response_data = await response.json()
                return BaseResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return BaseResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
            )

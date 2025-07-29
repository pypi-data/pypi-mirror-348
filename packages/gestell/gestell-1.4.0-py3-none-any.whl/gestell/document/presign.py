import aiohttp
import json

from gestell.types import BaseRequest, BaseResponse


class PresignDocumentRequest(BaseRequest):
    id: str
    filename: str
    type: str


class PresignDocumentResponse(BaseResponse):
    path: str
    url: str


async def presign_document(
    request: PresignDocumentRequest,
) -> PresignDocumentResponse:
    url = f'{request.api_url}/api/collection/{request.id}/document/presign'
    payload = {
        'filename': request.filename,
        'type': request.type,
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
                    return PresignDocumentResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error presigning the document'
                        ),
                        path='',
                        url='',
                    )

                response_data = await response.json()
                return PresignDocumentResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return PresignDocumentResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                path='',
                url='',
            )

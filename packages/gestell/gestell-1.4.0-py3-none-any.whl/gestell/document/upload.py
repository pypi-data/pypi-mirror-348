import aiohttp
import mimetypes
import os
from typing import Optional, Union

from gestell.document.create import create_document, CreateDocumentRequest
from gestell.document.presign import presign_document, PresignDocumentRequest
from gestell.types import BaseRequest, BaseResponse


class UploadDocumentRequest(BaseRequest):
    collection_id: str
    name: str
    file: Union[str, bytes]
    type: Optional[str] = None
    instructions: Optional[str] = None
    job: Optional[bool] = None
    tables: Optional[bool] = None


class UploadDocumentResponse(BaseResponse):
    id: str


async def upload_document(
    request: UploadDocumentRequest,
) -> UploadDocumentResponse:
    file_type = request.type
    if not file_type:
        if isinstance(request.file, str):
            file_type = mimetypes.guess_type(request.file)[0]
        else:
            file_type = 'text/plain'
    if not file_type:
        file_type = 'text/plain'

    presign_request = PresignDocumentRequest(
        api_key=request.api_key,
        api_url=request.api_url,
        debug=request.debug,
        id=request.collection_id,
        filename=request.name,
        type=file_type,
    )
    presign_response = await presign_document(presign_request)

    if presign_response.status != 'OK':
        return UploadDocumentResponse(
            status=presign_response.status,
            message=presign_response.message,
            id='',
        )

    url = presign_response.url

    async with aiohttp.ClientSession() as session:
        try:
            if isinstance(request.file, str):
                if os.path.exists(request.file):
                    with open(request.file, 'rb') as f:
                        file_content = f.read()

                        await session.put(
                            url,
                            headers={'Content-Type': file_type},
                            data=file_content,
                        )
                else:
                    return UploadDocumentResponse(
                        status='ERROR',
                        message='File does not exist',
                        id='',
                    )

            elif isinstance(request.file, bytes):
                await session.put(
                    url,
                    headers={'Content-Type': file_type},
                    data=request.file,
                )
            else:
                return UploadDocumentResponse(
                    status='ERROR',
                    message='Invalid file type provided, must be a string (path), or bytes.',
                    id='',
                )

        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return UploadDocumentResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                id='',
            )

    create_request = CreateDocumentRequest(
        api_key=request.api_key,
        api_url=request.api_url,
        debug=request.debug,
        collection_id=request.collection_id,
        name=request.name,
        path=presign_response.path,
        type=file_type,
        instructions=request.instructions,
        job=request.job,
        tables=request.tables,
    )

    create_response = await create_document(create_request)
    return create_response

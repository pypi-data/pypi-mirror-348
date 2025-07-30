import aiohttp
from typing import Optional, List

from gestell.types import BaseRequest, BaseResponse, Document, JobStatus


class GetDocumentsRequest(BaseRequest):
    id: str
    search: Optional[str] = None
    take: Optional[int] = None
    skip: Optional[int] = None
    extended: Optional[bool] = None
    status: Optional[JobStatus] = None
    nodes: Optional[JobStatus] = None
    edges: Optional[JobStatus] = None
    vectors: Optional[JobStatus] = None
    category: Optional[JobStatus] = None


class GetDocumentsResponse(BaseResponse):
    result: List[Document]


async def list_documents(request: GetDocumentsRequest) -> GetDocumentsResponse:
    url = f'{request.api_url}/api/collection/{request.id}/document'
    params = {}
    if request.search:
        params['search'] = request.search
    if request.take:
        params['take'] = str(request.take)
    if request.skip:
        params['skip'] = str(request.skip)
    if request.extended is not None:
        params['extended'] = str(request.extended).lower()
    if request.status:
        params['status'] = request.status
    if request.nodes:
        params['nodes'] = request.nodes
    if request.edges:
        params['edges'] = request.edges
    if request.vectors:
        params['vectors'] = request.vectors
    if request.category:
        params['category'] = request.category

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url,
                headers={'Authorization': f'BEARER {request.api_key}'},
                params=params,
            ) as response:
                if not response.ok:
                    error_response = await response.json()
                    if request.debug:
                        print(error_response)
                    return GetDocumentsResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error retrieving documents'
                        ),
                        result=[],
                    )
                response_data = await response.json()
                return GetDocumentsResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return GetDocumentsResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                result=[],
            )

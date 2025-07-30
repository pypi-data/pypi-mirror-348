import aiohttp
import json
from typing import List, Optional

from gestell.types import BaseRequest, BaseResponse, CollectionType, PiiIdentifierOption


class UpdateCollectionRequest(BaseRequest):
    collection_id: str
    organization_id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[CollectionType] = None
    pii: Optional[bool] = None
    pii_controls: Optional[List[PiiIdentifierOption]] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    graphInstructions: Optional[str] = None
    promptInstructions: Optional[str] = None
    searchInstructions: Optional[str] = None
    tags: Optional[List[str]] = None


class UpdateCollectionResponse(BaseResponse):
    pass


async def update_collection(
    request: UpdateCollectionRequest,
) -> UpdateCollectionResponse:
    url = f'{request.api_url}/api/collection/{request.collection_id}'

    payload = {
        'organizationId': request.organization_id,
        'name': request.name,
        'type': request.type,
        'pii': request.pii,
        'piiControls': request.pii_controls,
        'description': request.description,
        'instructions': request.instructions,
        'graphInstructions': request.graphInstructions,
        'promptInstructions': request.promptInstructions,
        'searchInstructions': request.searchInstructions,
        'tags': request.tags if request.tags else [],
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
                    return UpdateCollectionResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error updating the collection'
                        ),
                        id='',
                    )

                response_data = await response.json()
                return UpdateCollectionResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return UpdateCollectionResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                id='',
            )

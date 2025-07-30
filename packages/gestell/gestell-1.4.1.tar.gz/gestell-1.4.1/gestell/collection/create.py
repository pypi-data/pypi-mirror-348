import aiohttp
import json
from typing import List, Optional

from gestell.types import (
    BaseRequest,
    BaseResponse,
    CollectionType,
    CreateCategoryPayload,
    PiiIdentifierOption,
)


class CreateCollectionRequest(BaseRequest):
    organization_id: str
    name: str
    type: CollectionType
    pii: Optional[bool] = None
    pii_controls: Optional[List[PiiIdentifierOption]] = None
    tags: Optional[List[str]] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    graphInstructions: Optional[str] = None
    promptInstructions: Optional[str] = None
    searchInstructions: Optional[str] = None
    categories: Optional[List[CreateCategoryPayload]] = None


class CreateCollectionResponse(BaseResponse):
    id: str


async def create_collection(
    request: CreateCollectionRequest,
) -> CreateCollectionResponse:
    url = f'{request.api_url}/api/collection'

    payload = {
        'organizationId': request.organization_id,
        'name': request.name,
        'type': request.type,
        'tags': request.tags if request.tags else [],
        'pii': request.pii,
        'piiControls': request.pii_controls,
        'description': request.description,
        'instructions': request.instructions,
        'graphInstructions': request.graphInstructions,
        'promptInstructions': request.promptInstructions,
        'searchInstructions': request.searchInstructions,
        'categories': [cat.model_dump(by_alias=True) for cat in request.categories]
        if request.categories
        else [],
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
                    return CreateCollectionResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error creating a collection'
                        ),
                        id='',
                    )

                response_data = await response.json()
                return CreateCollectionResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return CreateCollectionResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                id='',
            )

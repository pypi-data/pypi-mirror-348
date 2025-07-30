import aiohttp
from typing import AsyncGenerator, List, Optional, Dict, Any
from gestell.types.query import PromptMessage
from pydantic import Field, ConfigDict

from gestell.types import BaseRequest, PromptRequestBody


class PromptQueryRequest(BaseRequest, PromptRequestBody):
    """
    Pydantic model for a prompt query.
    Inherits the base auth fields and all prompt-specific parameters.
    """

    collection_id: str = Field(..., alias='collectionId')
    category_id: Optional[str] = Field('', alias='categoryId')
    prompt: str = Field(...)
    method: Optional[str] = Field('normal')
    type: Optional[str] = Field('phrase')
    vector_depth: Optional[int] = Field(None, alias='vectorDepth')
    node_depth: Optional[int] = Field(None, alias='nodeDepth')
    max_queries: Optional[int] = Field(None, alias='maxQueries')
    max_results: Optional[int] = Field(None, alias='maxResults')
    template: Optional[str] = Field('')
    cot: Optional[bool] = Field(True, alias='cot')
    messages: List[PromptMessage] = Field(default_factory=list)
    thread_id: Optional[str] = Field(None, alias='threadId')

    model_config = ConfigDict(populate_by_name=True)


async def prompt_query(request: PromptQueryRequest) -> AsyncGenerator[bytes, None]:
    """
    Low-level HTTP caller for sending a PromptQueryRequest to Gestell.

    Uses the model's `model_dump` to:
      - output only the camel-cased fields
      - drop any None values
      - exclude internal fields (api_key, api_url, debug)
    """
    url = f'{request.api_url}/api/collection/{request.collection_id}/prompt'

    payload: Dict[str, Any] = request.model_dump(
        by_alias=True,
        exclude_none=True,
        exclude={'api_key', 'api_url', 'debug'},
    )

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                url,
                headers={
                    'Authorization': f'BEARER {request.api_key}',
                    'Content-Type': 'application/json',
                },
                json=payload,
            ) as resp:
                resp.raise_for_status()
                async for chunk in resp.content:
                    yield chunk
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            raise

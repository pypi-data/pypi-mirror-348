import aiohttp
from typing import Optional, List, Dict, Any
from pydantic import Field, ConfigDict

from gestell.types import BaseRequest, BaseResponse, SearchRequestBody, SearchResult


class SearchQueryRequest(BaseRequest, SearchRequestBody):
    """
    Pydantic model for a search query.
    Inherits the base auth fields and all search-specific parameters.
    """

    collection_id: str = Field(..., alias='collectionId')
    category_id: Optional[str] = Field('', alias='categoryId')
    prompt: str = Field(...)
    method: Optional[str] = Field('normal')
    type: Optional[str] = Field(...)
    vector_depth: Optional[int] = Field(None, alias='vectorDepth')
    node_depth: Optional[int] = Field(None, alias='nodeDepth')
    max_queries: Optional[int] = Field(None, alias='maxQueries')
    max_results: Optional[int] = Field(None, alias='maxResults')
    include_content: Optional[bool] = Field(True, alias='includeContent')
    include_edges: Optional[bool] = Field(False, alias='includeEdges')

    # allow populating via snake_case or camelCase
    model_config = ConfigDict(populate_by_name=True)


class SearchQueryResponse(BaseResponse):
    """
    Pydantic model for search query responses.
    """

    result: List[SearchResult]


async def search_query(request: SearchQueryRequest) -> SearchQueryResponse:
    """
    Low-level HTTP caller for sending a SearchQueryRequest to Gestell.
    """
    url = f'{request.api_url}/api/collection/{request.collection_id}/search'

    # build a clean camel-cased payload, dropping any None fields
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
                if not resp.ok:
                    error_data = await resp.json()
                    if request.debug:
                        print(error_data)
                    return SearchQueryResponse(
                        status='ERROR',
                        message=error_data.get(
                            'message', 'There was an error running the search query'
                        ),
                        result=[],
                    )

                data = await resp.json()
                return SearchQueryResponse(**data)

        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return SearchQueryResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                result=[],
            )

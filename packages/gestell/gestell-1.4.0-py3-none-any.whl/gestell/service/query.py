from typing import AsyncGenerator, List, Literal, Optional

from gestell.service.base import BaseService
from gestell.types import PromptMessage, SearchMethod, SearchType
from gestell.query.search import SearchQueryRequest, SearchQueryResponse, search_query
from gestell.query.prompt import PromptQueryRequest, prompt_query
from gestell.query.features import (
    FeaturesQueryRequest,
    FeaturesQueryResponse,
    featuresQuery,
)
from gestell.query.table import TablesQueryRequest, TablesQueryResponse, tables_query
from gestell.query.exportFeatures import ExportFeaturesRequest, export_features
from gestell.query.exportTable import ExportTableRequest, export_table


class QueryService(BaseService):
    """
    Query a collection. This requires your collection ID to query
    Note that querying tables and features requires both a collection_id and category_id.

    Learn more about usage at: https://gestell.ai/docs/reference#query
    """

    def __init__(self, api_key: str, api_url: str, debug: bool = False) -> None:
        super().__init__(api_key, api_url, debug)

    async def search(
        self,
        collection_id: str,
        prompt: str,
        *,
        category_id: Optional[str] = None,
        method: SearchMethod = 'normal',
        type: SearchType = 'phrase',
        vector_depth: Optional[int] = None,
        node_depth: Optional[int] = None,
        max_queries: Optional[int] = None,
        max_results: Optional[int] = None,
        include_content: Optional[bool] = None,
        include_edges: Optional[bool] = None,
    ) -> SearchQueryResponse:
        """Perform a search on a collection.

        Learn more about usage at: https://gestell.ai/docs/reference#query

        Executes a semantic and keyword search within the specified collection based on a prompt and optional filters.

        Args:
            collection_id: The unique identifier of the collection to search.
            prompt: The text prompt or query.
            category_id: Optional category ID to narrow down results.
            method: Search method to use (e.g., 'normal').
            type: Search type to specify (e.g., 'phrase').
            vector_depth: Optional depth for vector-based search.
            node_depth: Optional depth for node-based search.
            max_queries: Optional maximum number of sub-queries.
            max_results: Optional maximum number of results to return.
            include_content: If True, include document content in results.
            include_edges: If True, include edge relationships in results.

        Returns:
            SearchQueryResponse: Object containing status, message, and list of results.

        Raises:
            GestellError: If the search request fails.

        Example:
            ```python
            response = await query_service.search(
                collection_id='coll_123', prompt='Find relevant passages', max_results=5
            )
            for item in response.result:
                print(item.content)
            ```
        """
        req = SearchQueryRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            category_id=category_id,
            prompt=prompt,
            method=method,
            type=type,
            vector_depth=vector_depth,
            node_depth=node_depth,
            max_queries=max_queries,
            max_results=max_results,
            include_content=include_content,
            include_edges=include_edges,
        )
        return await search_query(req)

    async def prompt(
        self,
        collection_id: str,
        prompt: str,
        *,
        category_id: Optional[str] = None,
        method: SearchMethod = 'normal',
        type: SearchType = 'phrase',
        vector_depth: Optional[int] = None,
        node_depth: Optional[int] = None,
        max_queries: Optional[int] = None,
        max_results: Optional[int] = None,
        template: Optional[str] = None,
        cot: Optional[bool] = False,
        messages: Optional[List[PromptMessage]] = None,
        thread_id: Optional[str] = None,
        chat: Optional[str] = None,
    ) -> AsyncGenerator[bytes, None]:
        """Perform a streaming prompt query on a collection.

        Learn more about usage at: https://gestell.ai/docs/reference#query

        Sends a text prompt to the collection and returns an async stream of response chunks.

        Args:
            collection_id: The unique identifier of the collection to query.
            prompt: The text prompt to send to the model.
            category_id: Optional category ID to filter results by.
            method: Search method to use (e.g., 'normal').
            type: Search type to specify (e.g., 'phrase').
            vector_depth: Optional depth for vector-based search.
            node_depth: Optional depth for node-based search.
            max_queries: Optional maximum number of sub-queries.
            max_results: Optional maximum number of results to return.
            template: Optional prompt template string.
            cot: If True, enable chain-of-thought reasoning.
            messages: Optional list of chat history messages.
            thread_id: Optional thread ID to continue an existing conversation.
            chat: Optional chat session identifier.

        Returns:
            AsyncGenerator[bytes, None]: An async generator yielding raw response bytes.

        Raises:
            GestellError: If the prompt query fails.

        Example:
            ```python
            async for chunk in query_service.prompt(
                collection_id='coll_123', prompt='Summarize the document'
            ):
                print(chunk)
            ```
        """
        # build the typed request model
        req = PromptQueryRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            category_id=category_id,
            prompt=prompt,
            method=method,
            type=type,
            vector_depth=vector_depth,
            node_depth=node_depth,
            max_queries=max_queries,
            max_results=max_results,
            template=template,
            cot=cot,
            messages=messages,
            thread_id=thread_id,
            chat=chat,
        )

        # delegate to the low-level query function
        async for chunk in prompt_query(req):
            yield chunk

    async def features(
        self,
        collection_id: str,
        category_id: str,
        skip: Optional[int] = 0,
        take: Optional[int] = 10,
    ) -> FeaturesQueryResponse:
        """Retrieve feature metadata from a collection.

        Learn more about usage at: https://gestell.ai/docs/reference#query

        Fetches layout details for features in the specified category, including positions,
        labels, and descriptions.

        Args:
            collection_id: The unique identifier of the collection to query.
            category_id: The unique identifier of the category to retrieve features for.
            skip: Number of items to skip for pagination. Defaults to 0.
            take: Number of items to return. Defaults to 10.

        Returns:
            FeaturesQueryResponse: An object containing status, message, and a list of FeatureLayout.

        Raises:
            GestellError: If the features query fails.

        Example:
            ```python
            response = await query_service.features(
                collection_id='coll_123', category_id='cat_456', take=5
            )
            for feature in response.result:
                print(feature.label, feature.position)
            ```
        """
        request = FeaturesQueryRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            category_id=category_id,
            skip=skip,
            take=take,
        )
        response: FeaturesQueryResponse = await featuresQuery(request)
        return response

    async def features_export(
        self, collection_id: str, category_id: str, type: Literal['json', 'csv']
    ) -> any:
        """Export feature data from a collection.

        Learn more about usage at: https://gestell.ai/docs/reference#query

        Exports feature values in the specified format for a given category.

        Args:
            collection_id: The unique identifier of the collection to query.
            category_id: The unique identifier of the category to export features from.
            type: Output format, either 'json' or 'csv'.

        Returns:
            any: The exported feature data (JSON list or CSV string) depending on `type`.

        Raises:
            GestellError: If the export request fails.

        Example:
            ```python
            data = await query_service.features_export(
                collection_id='coll_123', category_id='cat_456', type='csv'
            )
            print(data)
            ```
        """
        request = ExportFeaturesRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            category_id=category_id,
            type=type,
        )
        response: any = await export_features(request)
        return response

    async def table(
        self,
        collection_id: str,
        category_id: str,
        skip: Optional[int] = 0,
        take: Optional[int] = 10,
        prompt: Optional[str] = None,
    ) -> TablesQueryResponse:
        """Retrieve table data from a collection.

        Learn more about usage at: https://gestell.ai/docs/reference#query

        Fetches table rows extracted from documents in the specified category.

        Args:
            collection_id: The unique identifier of the collection to query.
            category_id: The unique identifier of the category to retrieve tables for.
            skip: Number of table rows to skip for pagination. Defaults to 0.
            take: Number of table rows to return. Defaults to 10.
            prompt: Optional prompt to guide the table extraction. Defaults to None.

        Returns:
            TablesQueryResponse: An object containing status, message, and list of table rows.

        Raises:
            GestellError: If the table query fails.

        Example:
            ```python
            response = await query_service.table(
                collection_id='coll_123',
                category_id='cat_456',
                take=5,
                prompt='Extract financial data',
            )
            for row in response.result:
                print(row)
            ```
        """
        request = TablesQueryRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            category_id=category_id,
            skip=skip,
            take=take,
            prompt=prompt,
        )
        response: TablesQueryResponse = await tables_query(request)
        return response

    async def table_export(
        self, collection_id: str, category_id: str, type: Literal['json', 'csv']
    ) -> any:
        """Export table data from a collection.

        Learn more about usage at: https://gestell.ai/docs/reference#query

        Exports table rows in the specified format for a given category.

        Args:
            collection_id: The unique identifier of the collection to query.
            category_id: The unique identifier of the category to export tables from.
            type: Output format, either 'json' or 'csv'.

        Returns:
            any: The exported table data (JSON list or CSV string) depending on `type`.

        Raises:
            GestellError: If the export request fails.

        Example:
            ```python
            data = await query_service.table_export(
                collection_id='coll_123', category_id='cat_456', type='csv'
            )
            print(data)
            ```
        """
        request = ExportTableRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            category_id=category_id,
            type=type,
        )
        response: any = await export_table(request)
        return response

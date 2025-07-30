"""
Search and prompt schemas for interacting with the Gestell API.

Defines payloads and result models for collection search and prompt operations,
as well as default search mode constants.
"""

from typing import Dict, List, Literal, Optional, TypedDict

from pydantic import BaseModel, ConfigDict, Field


# Type Aliases

SearchType = Literal[
    'summary',  # Compare and analyze documents from their summaries
    'phrase',  # One-sentence prompt (RECOMMENDED)
    'keywords',  # Keyword-based search
]

SearchMethod = Literal[
    'fast',  # Prioritizes speed over depth
    'normal',  # Balanced depth and performance (RECOMMENDED)
    'precise',  # Full-depth search for maximum accuracy
]


# Default search parameter set for a given mode
class SearchDefaults(TypedDict):
    """Default parameter values for a search mode."""

    type: SearchType
    vector_depth: int
    node_depth: int
    max_queries: int
    max_results: int


# Search Mode Constants

SEARCH_FAST: SearchDefaults = {
    'type': 'phrase',
    'vector_depth': 10,
    'node_depth': 1,
    'max_queries': 1,
    'max_results': 10,
}

SEARCH_NORMAL: SearchDefaults = {
    'type': 'summary',
    'vector_depth': 8,
    'node_depth': 2,
    'max_queries': 3,
    'max_results': 10,
}

SEARCH_PRECISE: SearchDefaults = {
    'type': 'summary',
    'vector_depth': 10,
    'node_depth': 5,
    'max_queries': 3,
    'max_results': 10,
}

SEARCH_MODES: Dict[SearchMethod, SearchDefaults] = {
    'fast': SEARCH_FAST,
    'normal': SEARCH_NORMAL,
    'precise': SEARCH_PRECISE,
}


class SearchRequestBody(BaseModel):
    """
    Payload for executing a search against a collection.

    Includes filters, prompt, and performance/accuracy settings.
    """

    model_config = ConfigDict(populate_by_name=True)

    collection_id: str = Field(
        ..., alias='collectionId', description='Identifier of the target collection.'
    )
    category_id: Optional[str] = Field(
        None,
        alias='categoryId',
        description='Optional category filter within the collection.',
    )
    prompt: str = Field(..., description='Natural-language query or prompt.')
    method: SearchMethod = Field(
        'normal', description='Search performance/accuracy mode.'
    )
    type: Optional[SearchType] = Field(
        'phrase', description='Output format preference.'
    )
    vector_depth: Optional[int] = Field(
        8, alias='vectorDepth', ge=1, description='Number of vector hops to explore.'
    )
    node_depth: Optional[int] = Field(
        2, alias='nodeDepth', ge=1, description='Number of node hops to explore.'
    )
    max_queries: Optional[int] = Field(
        3,
        alias='maxQueries',
        ge=1,
        description='Maximum number of sub-queries to issue.',
    )
    max_results: Optional[int] = Field(
        10, alias='maxResults', ge=1, description='Maximum number of results to return.'
    )
    include_content: Optional[bool] = Field(
        False,
        alias='includeContent',
        description='Include full content in each result.',
    )
    include_edges: Optional[bool] = Field(
        False,
        alias='includeEdges',
        description='Include edge references in each result.',
    )
    edges_in_result: Optional[bool] = Field(
        False,
        alias='edgesInResult',
        description='Embed edge data within result objects.',
    )


class PromptMessage(BaseModel):
    """
    Single message in a prompt-driven interaction.

    Used to carry chat history or system instructions.
    """

    role: Literal['user', 'model', 'system'] = Field(
        ..., description='Origin of the message.'
    )
    content: str = Field(..., description='Textual content of the message.')


class PromptRequestBody(SearchRequestBody):
    """
    Payload for prompt-based operations, extending core search options.

    Adds template instructions, chain-of-thought flag, and message history.
    """

    template: Optional[str] = Field(
        None, description='Optional instruction template for the model.'
    )
    cot: Optional[bool] = Field(True, description='Enable chain-of-thought reasoning.')
    messages: Optional[List[PromptMessage]] = Field(
        [], description='Ordered list of past messages (oldest first).'
    )


class SearchResult(BaseModel):
    """
    Single entry in the search results array.

    Contains content snippet, citation, and reasoning.
    """

    content: str = Field(..., description='Extracted or generated content snippet.')
    citation: str = Field(
        ..., description='Source or citation reference for the content.'
    )
    reason: str = Field(..., description='Explanation of why this result was chosen.')

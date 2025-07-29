from typing import List, Optional

from gestell.service.base import BaseService
from gestell.types import (
    BaseResponse,
    CategoryType,
    CollectionType,
    CreateCategoryPayload,
    PiiIdentifierOption,
)
from gestell.collection.get import (
    GetCollectionRequest,
    GetCollectionResponse,
    get_collection,
)
from gestell.collection.list import (
    GetCollectionsRequest,
    GetCollectionsResponse,
    list_collections,
)
from gestell.collection.create import (
    CreateCollectionRequest,
    CreateCollectionResponse,
    create_collection,
)
from gestell.collection.update import (
    UpdateCollectionRequest,
    UpdateCollectionResponse,
    update_collection,
)
from gestell.collection.delete import (
    DeleteCollectionRequest,
    delete_collection,
)
from gestell.collection.addCategory import (
    AddCategoryRequest,
    AddCategoryResponse,
    add_category,
)
from gestell.collection.updateCategory import (
    UpdateCategoryRequest,
    UpdateCategoryResponse,
    update_category,
)
from gestell.collection.removeCategory import (
    RemoveCategoryRequest,
    RemoveCategoryResponse,
    remove_category,
)


class CollectionService(BaseService):
    """
    Manages collections you are a part of.

    Learn more about usage at: https://gestell.ai/docs/reference#collection
    """

    def __init__(self, api_key: str, api_url: str, debug: bool = False) -> None:
        super().__init__(api_key, api_url, debug)

    async def get(self, collection_id: str) -> GetCollectionResponse:
        """
        Fetch the details of a specific collection using its unique ID.

        Learn more about usage at: https://gestell.ai/docs/reference#collection

        Args:
            collection_id: The ID of the collection to retrieve.

        Returns:
            GetCollectionResponse: An object containing:
                - result (Optional[Collection]): The collection details if found, None otherwise.
                - stats (Optional[CollectionStats]): Statistics about the collection.
                - status (str): The status of the request ('SUCCESS', 'ERROR', etc.).
                - message (Optional[str]): Additional details about the request result.

        Note:
            The Collection object contains fields like id, name, type, description,
            organization details, and various instruction sets. The CollectionStats
            object contains metrics about the collection's size and processing status.

            For complete field documentation, see the Collection and CollectionStats
            type definitions.
        """
        request = GetCollectionRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
        )
        response: GetCollectionResponse = await get_collection(request)
        return response

    async def list(
        self,
        search: Optional[str] = None,
        take: Optional[int] = 10,
        skip: Optional[int] = 0,
        extended: Optional[bool] = None,
    ) -> GetCollectionsResponse:
        """
        Fetch a list of collections with optional filtering and pagination.

        Learn more about usage at: https://gestell.ai/docs/reference#collection

        Args:
            search: Optional search query to filter collections by name, description, or tags.
            take: Maximum number of collections to return (default: 10).
            skip: Number of collections to skip for pagination (default: 0).
            extended: If True, includes additional details for each collection.

        Returns:
            GetCollectionsResponse: An object containing:
                - result (List[Collection]): List of collection objects matching the query.
                - status (str): The status of the request ('SUCCESS', 'ERROR', etc.).
                - message (Optional[str]): Additional details about the request result.

        Note:
            Each Collection object in the result contains fields like id, name, type,
            description, organization details, and various instruction sets. The exact
            fields returned depend on whether extended details are requested.

            For complete field documentation, see the Collection type definition.
        """
        request = GetCollectionsRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            search=search,
            take=take,
            skip=skip,
            extended=extended,
        )
        response: GetCollectionsResponse = await list_collections(request)
        return response

    async def create(
        self,
        organization_id: str,
        name: str,
        type: Optional[CollectionType] = 'canon',
        tags: Optional[List[str]] = None,
        pii: Optional[bool] = None,
        pii_controls: Optional[List[PiiIdentifierOption]] = None,
        description: Optional[str] = None,
        instructions: Optional[str] = None,
        graphInstructions: Optional[str] = None,
        promptInstructions: Optional[str] = None,
        searchInstructions: Optional[str] = None,
        categories: Optional[List[CreateCategoryPayload]] = None,
    ) -> CreateCollectionResponse:
        """
        Create a new collection with the specified configuration.

        Learn more about usage at: https://gestell.ai/docs/reference#collection

        Args:
            organization_id: The ID of the organization that will own the collection.
            name: The display name for the new collection.
            type: The type of collection to create. Must be one of:
                - 'frame': Basic OCR outputs only
                - 'searchable-frame': Lighter search-optimized version
                - 'canon': Full canonized dataset
                - 'features': Feature-extraction mode
            tags: Optional list of tags to associate with the collection.
            pii: Optional boolean flag to enable PII detection and handling.
            pii_controls: Optional list of PII identifiers to control. Available options:
                - 'Name', 'Geographic Data', 'Dates', 'Phone Number', 'Fax Number',
                'Email Address', 'Social Security Number', 'Medical Record Number',
                'Health Plan Beneficiary Number', 'Account Number',
                'Certificate/License Number', 'Vehicle Identifier',
                'Device Identifier', 'Web URL', 'IP Address', 'Biometric Identifier',
                'Full-face Photograph', 'Unique Identifier Code'
            description: Optional detailed description of the collection's purpose.
            instructions: Optional general instructions for the collection.
            graphInstructions: Optional instructions specific to graph operations.
            promptInstructions: Optional instructions for prompt-related operations.
            searchInstructions: Optional instructions for search operations.
            categories: Optional list of categories to create within the collection. Each category
                requires a name, type, and instructions. Category types can be:
                - 'content': Filter content by instructions
                - 'concepts': Conceptual summaries
                - 'features': Label extraction
                - 'table': Tabular data

        Returns:
            CreateCollectionResponse: An object containing:
                - id (str): The unique identifier of the newly created collection.
                - status (str): The status of the request ('SUCCESS', 'ERROR', etc.).
                - message (Optional[str]): Additional details about the request result.

        Note:
            The collection will be created with the specified configuration and will be immediately
            available for use. The response will include the new collection's ID which should be
            used for subsequent operations on this collection.

            For complete field documentation, see the CreateCategoryPayload type definition.
        """
        request = CreateCollectionRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            organization_id=organization_id,
            name=name,
            type=type,
            tags=tags,
            pii=pii,
            pii_controls=pii_controls,
            description=description,
            instructions=instructions,
            graphInstructions=graphInstructions,
            promptInstructions=promptInstructions,
            searchInstructions=searchInstructions,
            categories=categories,
        )
        response: CreateCollectionResponse = await create_collection(request)
        return response

    async def update(
        self,
        collection_id: str,
        organization_id: Optional[str] = None,
        name: Optional[str] = None,
        type: Optional[CollectionType] = None,
        pii: Optional[bool] = None,
        pii_controls: Optional[List[PiiIdentifierOption]] = None,
        description: Optional[str] = None,
        instructions: Optional[str] = None,
        graphInstructions: Optional[str] = None,
        promptInstructions: Optional[str] = None,
        searchInstructions: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> UpdateCollectionResponse:
        """
        Update an existing collection with the provided details.

        This method allows updating various attributes of an existing collection, including its name, type,
        description, and various instruction sets. All parameters except `collection_id` are optional and only
        the provided fields will be updated.

        Learn more about collections at: https://gestell.ai/docs/reference#collection

        Args:
            collection_id: The unique identifier of the collection to update.
            organization_id: The organization ID to associate with the collection.
            name: The new name for the collection.
            type: The type of collection. Must be one of:
                - 'frame': Basic OCR outputs only
                - 'searchable-frame': Lighter search-optimized version
                - 'canon': Full canonized dataset
                - 'features': Feature-extraction mode
            pii: Optional boolean flag to enable/disable PII detection and handling.
            pii_controls: Optional list of PII identifiers to control. Available options:
                - 'Name', 'Geographic Data', 'Dates', 'Phone Number', 'Fax Number',
                'Email Address', 'Social Security Number', 'Medical Record Number',
                'Health Plan Beneficiary Number', 'Account Number',
                'Certificate/License Number', 'Vehicle Identifier',
                'Device Identifier', 'Web URL', 'IP Address', 'Biometric Identifier',
                'Full-face Photograph', 'Unique Identifier Code'
            description: A detailed description of the collection's purpose.
            instructions: General instructions for the collection.
            graphInstructions: Instructions specific to graph operations.
            promptInstructions: Instructions for prompt-related operations.
            searchInstructions: Instructions for search operations.
            tags: List of tags to associate with the collection.

        Returns:
            UpdateCollectionResponse: An object containing the status and optional message of the update.

        Note:
            - Only the provided fields will be updated; unspecified fields remain unchanged.
            - The collection ID cannot be changed after creation.
            - To update PII controls, you must also set `pii=True`.
        """
        request = UpdateCollectionRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            organization_id=organization_id,
            name=name,
            type=type,
            pii=pii,
            pii_controls=pii_controls,
            description=description,
            instructions=instructions,
            graphInstructions=graphInstructions,
            promptInstructions=promptInstructions,
            searchInstructions=searchInstructions,
            tags=tags,
        )
        response: UpdateCollectionResponse = await update_collection(request)
        return response

    async def delete(self, collection_id: str) -> BaseResponse:
        """
        Delete an existing collection by its unique ID.

        This method sends a request to delete the specified collection. The operation is
        irreversible and will permanently remove the collection and all its associated data.

        Learn more about collections at: https://gestell.ai/docs/reference#collection

        Args:
            collection_id: The unique identifier of the collection to delete.

        Returns:
            BaseResponse: An object containing the status and optional message of the deletion.
                - `status`: Either 'SUCCESS' if the deletion was successful, or 'ERROR' if it failed.
                - `message`: An optional message providing additional details about the operation.

        Note:
            - This operation cannot be undone. All data in the collection will be permanently deleted.
            - The collection ID cannot be reused after deletion.
        """
        request = DeleteCollectionRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
        )
        response = await delete_collection(request)
        return response

    async def add_category(
        self,
        collection_id: str,
        name: str,
        type: CategoryType,
        instructions: str,
        single_entry: Optional[bool] = None,
    ) -> AddCategoryResponse:
        """
        Add a new category to the specified collection.

        This method creates a new category within an existing collection. The category will be
        associated with the provided collection and can be used for organizing and classifying
        content within that collection.

        Args:
            collection_id: The unique identifier of the collection to which the category
                will be added.
            name: The display name of the category. Should be unique within the collection.
            type: The type of the category, as defined by the CategoryType enum.
            instructions: Detailed instructions or description for the category. This provides
                context about how the category should be used.
            single_entry: If True, only a single entry is allowed in this category.
                Defaults to None (false).

        Returns:
            AddCategoryResponse: An object containing the unique identifier of the
                newly created category.

        Raises:
            GestellError: If the request fails due to invalid parameters, authentication issues,
                or server errors.

        Example:
            ```python
            response = await collection_service.add_category(
                collection_id='coll_123',
                name='Product Reviews',
                type=CategoryType.TEXT,
                instructions='Categorize product reviews based on sentiment',
            )
            print(f'Created category with ID: {response.id}')
            ```
        """
        request = AddCategoryRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            name=name,
            type=type,
            instructions=instructions,
            single_entry=single_entry,
        )
        response: AddCategoryResponse = await add_category(request)
        return response

    async def update_category(
        self,
        collection_id: str,
        category_id: str,
        name: Optional[str] = None,
        type: Optional[CategoryType] = None,
        instructions: Optional[str] = None,
        single_entry: Optional[bool] = None,
    ) -> UpdateCategoryResponse:
        """
        Update an existing category within a collection.

        This method allows you to modify the properties of an existing category, including
        its name, type, instructions, and single_entry setting. At least one of the optional
        parameters must be provided to make a valid update.

        Args:
            collection_id: The unique identifier of the collection containing the category.
            category_id: The unique identifier of the category to update.
            name: The new name for the category. If None, the existing name will be preserved.
            type: The new type for the category, as defined by the CategoryType enum.
                If None, the existing type will be preserved.
            instructions: New instructions or description for the category. If None, the
                existing instructions will be preserved.
            single_entry: If True, only a single entry is allowed in this category.
                If None, the existing setting will be preserved.

        Returns:
            UpdateCategoryResponse: An object containing the status of the update operation.

        Raises:
            GestellError: If the request fails due to invalid parameters, authentication issues,
                or if the specified collection or category is not found.

        Example:
            ```python
            response = await collection_service.update_category(
                collection_id='coll_123',
                category_id='cat_456',
                name='Updated Category Name',
                instructions='Updated instructions for this category',
            )
            print(f'Update status: {response.status}')
            ```
        """
        request = UpdateCategoryRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            category_id=category_id,
            name=name,
            type=type,
            instructions=instructions,
            single_entry=single_entry,
        )
        response: UpdateCategoryResponse = await update_category(request)
        return response

    async def remove_category(
        self, collection_id: str, category_id: str
    ) -> RemoveCategoryResponse:
        """
        Remove a category from a collection.

        This method permanently deletes a category from the specified collection.
        Note that this action cannot be undone, and any content associated with this
        category will no longer be categorized.


        Args:
            collection_id: The unique identifier of the collection containing the category.
            category_id: The unique identifier of the category to be removed.

        Returns:
            RemoveCategoryResponse: An object containing the status of the removal operation.

        Raises:
            GestellError: If the request fails due to invalid parameters, authentication issues,
                or if the specified collection or category is not found.

        Example:
            ```python
            response = await collection_service.remove_category(
                collection_id='coll_123',
                category_id='cat_456',
            )
            if response.status == 'OK':
                print('Category removed successfully')
            else:
                print(f'Failed to remove category: {response.message}')
            ```
        """
        request = RemoveCategoryRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            category_id=category_id,
        )
        response: RemoveCategoryResponse = await remove_category(request)
        return response

from typing import Any, Optional, Union, Literal

from gestell.service.base import BaseService
from gestell.types import (
    BaseResponse,
    JobStatus,
)
from gestell.document.get import (
    GetDocumentRequest,
    GetDocumentResponse,
    get_document,
)
from gestell.document.export import (
    ExportDocumentRequest,
    export_document,
)
from gestell.document.list import (
    GetDocumentsRequest,
    GetDocumentsResponse,
    list_documents,
)
from gestell.document.upload import (
    UploadDocumentRequest,
    UploadDocumentResponse,
    upload_document,
)
from gestell.document.create import (
    CreateDocumentRequest,
    CreateDocumentResponse,
    create_document,
)
from gestell.document.delete import (
    DeleteDocumentRequest,
    delete_document,
)
from gestell.document.presign import (
    PresignDocumentRequest,
    PresignDocumentResponse,
    presign_document,
)
from gestell.document.update import (
    UpdateDocumentRequest,
    update_document,
)


class DocumentService(BaseService):
    """
    Manage documents within a collection. You will need to retrieve the collection id to manage documents.

    Learn more about usage at: https://gestell.ai/docs/reference#document
    """

    def __init__(self, api_key: str, api_url: str, debug: bool = False) -> None:
        super().__init__(api_key, api_url, debug)

    async def get(self, collection_id: str, document_id: str) -> GetDocumentResponse:
        """
        Retrieve a specific document from a collection.

        Learn more about usage at: https://gestell.ai/docs/reference#document

        Fetches the details of a document using its unique identifier within the specified
        collection. The document must exist in the collection and be accessible with the
        provided API key.

        Args:
            collection_id: The unique identifier of the collection containing the document.
            document_id: The unique identifier of the document to retrieve.

        Returns:
            GetDocumentResponse: An object containing the document details and request status.

        Raises:
            GestellError: If the request fails due to invalid parameters, authentication issues,
                or if the specified document or collection is not found.

        Example:
            ```python
            response = await document_service.get(
                collection_id='coll_123', document_id='doc_456'
            )
            if response.status == 'OK' and response.result:
                document = response.result[0]
                print(f'Retrieved document: {document.name}')
            ```
        """
        request = GetDocumentRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            document_id=document_id,
        )
        response: GetDocumentResponse = await get_document(request)
        return response

    async def export(
        self, collection_id: str, document_id: str, type: Literal['json', 'text']
    ) -> Any:
        """
        Export a document in a specified format.

        Learn more about usage at: https://gestell.ai/docs/reference#document

        Retrieves a document from the specified collection and returns it in either
        JSON or plain text format, depending on the requested type.

        Args:
            collection_id: The unique identifier of the collection containing the document.
            document_id: The unique identifier of the document to export.
            type: The export format. Must be either 'json' or 'text'.

        Returns:
            Any: The document content in the requested format. The exact type depends on the
                export type and document content.

        Raises:
            GestellError: If the request fails, the document/collection is not found,
                or an invalid export type is specified.

        Example:
            ```python
            # Export as JSON
            json_export = await document_service.export(
                collection_id='coll_123', document_id='doc_456', type='json'
            )

            # Export as plain text
            text_export = await document_service.export(
                collection_id='coll_123', document_id='doc_456', type='text'
            )
            ```
        """
        request = ExportDocumentRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            document_id=document_id,
            type=type,
        )
        response: any = await export_document(request)
        return response

    async def list(
        self,
        collection_id: str,
        search: Optional[str] = None,
        take: Optional[int] = 10,
        skip: Optional[int] = 0,
        extended: Optional[bool] = None,
        status: Optional[JobStatus] = None,
        nodes: Optional[JobStatus] = None,
        edges: Optional[JobStatus] = None,
        vectors: Optional[JobStatus] = None,
        category: Optional[JobStatus] = None,
    ) -> GetDocumentsResponse:
        """
        List documents in a collection with optional filtering and pagination.

        Learn more about usage at: https://gestell.ai/docs/reference#document

        Retrieves a paginated list of documents from the specified collection, with various
        filtering options to narrow down the results. The response includes document
        metadata and status information.

        Args:
            collection_id: The unique identifier of the collection to list documents from.
            search: Optional search query to filter documents by name or content.
            take: Maximum number of documents to return. Defaults to 10.
            skip: Number of documents to skip for pagination. Defaults to 0.
            extended: If True, includes additional metadata in the response.
            status: Filter documents by their processing status.
            nodes: Filter documents by node processing status.
            edges: Filter documents by edge processing status.
            vectors: Filter documents by vector processing status.
            category: Filter documents by category processing status.

        Returns:
            GetDocumentsResponse: An object containing the list of matching documents and
                pagination information.

        Raises:
            GestellError: If the request fails or the collection is not found.

        Example:
            ```python
            # Get first page of documents
            response = await document_service.list(
                collection_id='coll_123', take=20, skip=0
            )

            # Search for documents
            search_results = await document_service.list(
                collection_id='coll_123', search='quarterly report', take=10
            )

            # Filter by status
            processed_docs = await document_service.list(
                collection_id='coll_123', status=JobStatus.COMPLETED
            )
            ```
        """
        request = GetDocumentsRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            id=collection_id,
            search=search,
            take=take,
            skip=skip,
            extended=extended,
            status=status,
            nodes=nodes,
            edges=edges,
            vectors=vectors,
            category=category,
        )
        response: GetDocumentsResponse = await list_documents(request)
        return response

    async def upload(
        self,
        collection_id: str,
        name: str,
        file: Union[str, bytes],
        type: Optional[str] = None,
        instructions: Optional[str] = None,
        job: Optional[bool] = None,
        tables: Optional[bool] = None,
    ) -> UploadDocumentResponse:
        """
        Upload a document to the specified collection.

        Learn more about usage at: https://gestell.ai/docs/reference#document

        This method handles the upload of a document, which can be provided either as a file path
        or as bytes. The document will be associated with the specified collection and can be
        processed immediately if requested.

        Args:
            collection_id: The unique identifier of the target collection.
            name: The name to assign to the uploaded document.
            file: The document to upload, either as a file path (str) or raw bytes.
            type: The MIME type of the file (e.g., 'application/pdf', 'text/plain').
                If not provided, it will be inferred from the file extension when possible.
            instructions: Optional instructions or notes about the document.
            job: If True, starts document processing immediately after upload.
                Set to False to upload without processing.
            tables: If True, enables enhanced table extraction for PDF documents.
                Recommended for documents containing complex tabular data.

        Returns:
            UploadDocumentResponse: An object containing the upload status and document ID.

        Raises:
            GestellError: If the upload fails due to invalid parameters, authentication issues,
                or if the specified collection is not found.

        Example:
            ```python
            # Upload from file path
            response = await document_service.upload(
                collection_id='coll_123',
                name='report.pdf',
                file='/path/to/document.pdf',
                type='application/pdf',
                tables=True,
            )

            # Upload from bytes
            with open('document.pdf', 'rb') as f:
                file_data = f.read()
            response = await document_service.upload(
                collection_id='coll_123',
                name='report.pdf',
                file=file_data,
                type='application/pdf',
            )
            ```
        """
        request = UploadDocumentRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            name=name,
            file=file,
            type=type,
            instructions=instructions,
            job=job,
            tables=tables,
        )
        response: UploadDocumentResponse = await upload_document(request)
        return response

    async def presign(
        self,
        collection_id: str,
        filename: str,
        type: str,
    ) -> PresignDocumentResponse:
        """
        Generate a pre-signed URL for direct document uploads.

        Learn more about usage at: https://gestell.ai/docs/reference#document

        This method generates a pre-signed URL that can be used to upload a document
        directly to cloud storage. This is useful for large files or when you need to
        upload from a client-side application.

        Args:
            collection_id: The unique identifier of the target collection.
            filename: The name of the file to be uploaded.
            type: The MIME type of the file (e.g., 'application/pdf', 'image/png').

        Returns:
            PresignDocumentResponse: An object containing the pre-signed URL and upload details.

        Raises:
            GestellError: If the request fails due to invalid parameters or authentication issues.

        Example:
            ```python
            # Get a pre-signed URL
            response = await document_service.presign(
                collection_id='coll_123', filename='report.pdf', type='application/pdf'
            )

            # Use the pre-signed URL to upload a file
            import requests

            with open('report.pdf', 'rb') as f:
                files = {'file': f}
                upload_response = requests.put(
                    response.url, data=f, headers={'Content-Type': 'application/pdf'}
                )
            ```
        """
        request = PresignDocumentRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            id=collection_id,
            filename=filename,
            type=type,
        )
        response: PresignDocumentResponse = await presign_document(request)
        return response

    async def create(
        self,
        collection_id: str,
        name: str,
        path: str,
        type: str,
        instructions: Optional[str] = None,
        job: Optional[bool] = None,
        tables: Optional[bool] = None,
    ) -> CreateDocumentResponse:
        """
        Create a new document record in the specified collection.

        Learn more about usage at: https://gestell.ai/docs/reference#document

        This method creates a document record that references a file already present in storage.
        Use this when you've already uploaded a file using a pre-signed URL or another method.

        Args:
            collection_id: The unique identifier of the target collection.
            name: The display name for the document.
            path: The storage path where the document is located.
            type: The MIME type of the document (e.g., 'application/pdf', 'text/plain').
            instructions: Optional instructions or notes about the document.
            job: If True, starts document processing immediately after creation.
                Set to False to create the document without processing.
            tables: If True, enables enhanced table extraction for the document.
                Recommended for documents containing complex tabular data.

        Returns:
            CreateDocumentResponse: An object containing the creation status and document ID.

        Raises:
            GestellError: If the creation fails due to invalid parameters, authentication issues,
                or if the specified collection is not found.

        Example:
            ```python
            response = await document_service.create(
                collection_id='coll_123',
                name='Annual Report',
                path='documents/report.pdf',
                type='application/pdf',
                instructions='Process with table extraction',
                tables=True,
            )
            print(f'Created document with ID: {response.id}')
            ```
        """
        request = CreateDocumentRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            name=name,
            path=path,
            type=type,
            instructions=instructions,
            job=job,
            tables=tables,
        )
        response: CreateDocumentResponse = await create_document(request)
        return response

    async def update(
        self,
        collection_id: str,
        document_id: str,
        name: Optional[str] = None,
        instructions: Optional[str] = None,
        job: Optional[bool] = None,
        tables: Optional[bool] = None,
    ) -> BaseResponse:
        """
        Update an existing document's metadata or trigger reprocessing.

        Learn more about usage at: https://gestell.ai/docs/reference#document

        This method allows updating various attributes of an existing document,
        including its name, instructions, and processing settings. At least one
        optional parameter must be provided for a valid update.

        Args:
            collection_id: The unique identifier of the collection containing the document.
            document_id: The unique identifier of the document to update.
            name: The new name for the document. If None, the existing name is preserved.
            instructions: New instructions or notes about the document.
                If None, existing instructions are preserved.
            job: If True, triggers reprocessing of the document with the updated settings.
            tables: If True, enables enhanced table extraction during the next processing.
                Only applicable if job is set to True.

        Returns:
            BaseResponse: An object containing the status of the update operation.

        Raises:
            GestellError: If the update fails, the document/collection is not found,
                or if no update parameters are provided.

        Example:
            ```python
            # Update document name and instructions
            response = await document_service.update(
                collection_id='coll_123',
                document_id='doc_456',
                name='Updated Report Name',
                instructions='New processing instructions',
            )

            # Trigger reprocessing with table extraction
            response = await document_service.update(
                collection_id='coll_123', document_id='doc_456', job=True, tables=True
            )
            ```
        """
        request = UpdateDocumentRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            id=collection_id,
            document_id=document_id,
            name=name,
            instructions=instructions,
            job=job,
            tables=tables,
        )
        response: BaseResponse = await update_document(request)
        return response

    async def delete(self, collection_id: str, document_id: str) -> BaseResponse:
        """
        Permanently delete a document from a collection.

        Learn more about usage at: https://gestell.ai/docs/reference#document

        This action is irreversible and will permanently remove the document and all its
        associated data from the system. Use with caution.

        Args:
            collection_id: The unique identifier of the collection containing the document.
            document_id: The unique identifier of the document to delete.

        Returns:
            BaseResponse: An object containing the status of the delete operation.

        Raises:
            GestellError: If the deletion fails, or if the specified document or collection
                is not found.

        Example:
            ```python
            response = await document_service.delete(
                collection_id='coll_123', document_id='doc_456'
            )
            if response.status == 'OK':
                print('Document deleted successfully')
            ```
        """
        request = DeleteDocumentRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            document_id=document_id,
        )
        response: BaseResponse = await delete_document(request)
        return response

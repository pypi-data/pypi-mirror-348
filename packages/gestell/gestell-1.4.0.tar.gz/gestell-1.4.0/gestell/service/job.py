from typing import List, Optional

from gestell.service.base import BaseService
from gestell.types import (
    BaseResponse,
    JobStatus,
    JobType,
)
from gestell.job.cancel import (
    cancel_jobs,
    CancelJobsRequest,
    CancelJobsResponse,
)
from gestell.job.get import get_job, GetJobRequest, GetJobResponse
from gestell.job.list import list_jobs, GetJobsRequest, GetJobsResponse
from gestell.job.reprocess import (
    reprocess_document,
    ReprocessDocumentsRequest,
    ReprocessDocumentsResponse,
)


class JobService(BaseService):
    """
    Manage jobs within a collection. You will need to retrieve the collection id to manage jobs.

    Learn more about usage at: https://gestell.ai/docs/reference#job
    """

    def __init__(self, api_key: str, api_url: str, debug: bool = False) -> None:
        super().__init__(api_key, api_url, debug)

    async def get(self, collection_id: str, document_id: str) -> GetJobResponse:
        """
        Retrieve the status and details of a specific job.

        Learn more about usage at: https://gestell.ai/docs/reference#job

        This method fetches the current status and details of a job associated with
        a specific document in a collection. Jobs represent background processing tasks
        such as document analysis, vectorization, or categorization.

        Args:
            collection_id: The unique identifier of the collection containing the job.
            document_id: The unique identifier of the document associated with the job.

        Returns:
            GetJobResponse: An object containing the job details and status.

        Raises:
            GestellError: If the request fails or the specified job is not found.

        Example:
            ```python
            response = await job_service.get(
                collection_id='coll_123', document_id='doc_456'
            )
            print(f'Job status: {response.result.status}')
            print(f'Last updated: {response.result.dateUpdated}')
            ```
        """
        request = GetJobRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            document_id=document_id,
        )
        response: GetJobResponse = await get_job(request)
        return response

    async def list(
        self,
        collection_id: str,
        take: Optional[int] = 10,
        skip: Optional[int] = 0,
        status: Optional[JobStatus] = 'all',
        nodes: Optional[JobStatus] = 'all',
        edges: Optional[JobStatus] = 'all',
        vectors: Optional[JobStatus] = 'all',
        category: Optional[JobStatus] = 'all',
    ) -> GetJobsResponse:
        """
        List jobs in a collection with optional filtering and pagination.

        Learn more about usage at: https://gestell.ai/docs/reference#job

        Retrieves a paginated list of jobs for the specified collection, with various
        filtering options to narrow down the results. Jobs can be filtered by their
        overall status or by the status of specific processing components.

        Args:
            collection_id: The unique identifier of the collection.
            take: Maximum number of jobs to return. Defaults to 10.
            skip: Number of jobs to skip for pagination. Defaults to 0.
            status: Filter jobs by their overall status. Defaults to 'all'.
            nodes: Filter by node processing status. Defaults to 'all'.
            edges: Filter by edge processing status. Defaults to 'all'.
            vectors: Filter by vector processing status. Defaults to 'all'.
            category: Filter by category processing status. Defaults to 'all'.

        Returns:
            GetJobsResponse: An object containing the list of matching jobs and pagination info.

        Raises:
            GestellError: If the request fails or the collection is not found.

        Example:
            ```python
            # Get first page of all jobs
            response = await job_service.list(collection_id='coll_123')

            # Get only completed jobs
            completed_jobs = await job_service.list(
                collection_id='coll_123', status=JobStatus.COMPLETED
            )

            # Get jobs with pagination
            second_page = await job_service.list(
                collection_id='coll_123', take=20, skip=20
            )
            ```
        """
        request = GetJobsRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            take=take,
            skip=skip,
            status=status,
            nodes=nodes,
            edges=edges,
            vectors=vectors,
            category=category,
        )
        response: GetJobsResponse = await list_jobs(request)
        return response

    async def reprocess(
        self, collection_id: str, ids: List[str], type: JobType
    ) -> ReprocessDocumentsResponse:
        """
        Reprocess one or more documents in a collection.

        Learn more about usage at: https://gestell.ai/docs/reference#job

        This method allows you to trigger reprocessing of specific document components,
        such as nodes, edges, or vectors. This is useful when you need to update the
        processing results without re-uploading the documents.

        Args:
            collection_id: The unique identifier of the collection containing the documents.
            ids: A list of document IDs to be reprocessed.
            type: The type of processing to be performed. Must be one of:
                - 'status': Overall document status
                - 'nodes': Document nodes processing
                - 'edges': Document edges processing
                - 'vectors': Document vector embeddings
                - 'category': Document categorization

        Returns:
            ReprocessDocumentsResponse: An object containing the status of the operation.

        Raises:
            GestellError: If the request fails, the collection is not found,
                or an invalid job type is specified.

        Example:
            ```python
            # Reprocess vector embeddings for specific documents
            response = await job_service.reprocess(
                collection_id='coll_123',
                ids=['doc_1', 'doc_2', 'doc_3'],
                type=JobType.VECTORS,
            )

            # Check if reprocessing was initiated successfully
            if response.status == 'OK':
                print('Reprocessing started successfully')
            ```
        """
        request = ReprocessDocumentsRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            ids=ids,
            type=type,
        )
        response: ReprocessDocumentsResponse = await reprocess_document(request)
        return response

    async def cancel(self, collection_id: str, ids: List[str]) -> BaseResponse:
        """
        Cancel one or more running or queued jobs.

        Learn more about usage at: https://gestell.ai/docs/reference#job

        This method attempts to cancel the specified jobs. Only jobs that are in a pending
        or running state can be cancelled. Completed or failed jobs cannot be cancelled.

        Args:
            collection_id: The unique identifier of the collection containing the jobs.
            ids: A list of job IDs to be cancelled.

        Returns:
            BaseResponse: An object containing the status of the cancellation request.

        Raises:
            GestellError: If the request fails or the specified jobs/collection are not found.

        Example:
            ```python
            # Cancel specific jobs
            response = await job_service.cancel(
                collection_id='coll_123', ids=['job_1', 'job_2', 'job_3']
            )

            if response.status == 'OK':
                print('Jobs cancelled successfully')
            ```
        """
        request = CancelJobsRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            collection_id=collection_id,
            ids=ids,
        )
        response: CancelJobsResponse = await cancel_jobs(request)
        return response

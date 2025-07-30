from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field

from gestell.types.layout import LayoutType

# Type Aliases
JobType = Literal[
    'status',  # The OCR job status
    'nodes',  # Canonization and node extraction step
    'vectors',  # Vector generation step
    'edges',  # Edge linking step
    'category',  # Category assignment step
]

JobStatus = Literal[
    'processing',  # Currently in progress
    'error',  # Encountered an error
    'ready',  # Completed successfully
    'cancelled',  # Manually cancelled
    'unprocessed',  # Not yet started
    'partial',  # Partially completed
    'all',  # All steps completed
]


class JobDocument(BaseModel):
    """Snapshot of document metadata at job creation time.

    This represents a lightweight view of a document associated with a job.
    """

    id: str = Field(..., description='Document identifier.')
    collection_id: str = Field(
        ..., alias='collectionId', description='Collection identifier.'
    )
    date_created: datetime = Field(
        ..., alias='dateCreated', description='Creation timestamp.'
    )
    date_updated: datetime = Field(
        ..., alias='dateUpdated', description='Last update timestamp.'
    )
    name: str = Field(..., description='Document name or filename.')
    type: str = Field(..., description='MIME type or custom type label.')
    layout_type: LayoutType = Field(
        ..., alias='layoutType', description='Layout parsing strategy used.'
    )
    layout_nodes: int = Field(
        ..., alias='layoutNodes', description='Number of layout nodes generated.'
    )
    instructions: str = Field(..., description='Custom instructions for processing.')

    class Config:
        validate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class Job(BaseModel):
    """Represents a processing job for a specific document within a collection.

    This model tracks the status of various processing steps for a document,
    including node extraction, vector generation, edge linking, and categorization.
    """

    id: str = Field(..., description='Unique identifier for the job.')
    collection_id: str = Field(
        ..., alias='collectionId', description='Identifier of the parent collection.'
    )
    document_id: str = Field(
        ..., alias='documentId', description='Identifier of the target document.'
    )

    # Status fields
    status: JobStatus = Field(
        ..., description='Overall job status (equivalent to most critical step status).'
    )
    nodes: JobStatus = Field(..., description='Status of the node extraction step.')
    edges: JobStatus = Field(..., description='Status of the edge linking step.')
    vectors: JobStatus = Field(..., description='Status of the vector generation step.')
    category: JobStatus = Field(
        ..., description='Status of the category assignment step.'
    )

    message: str = Field(..., description='Human-readable message or error details.')

    # Optional document snapshot
    document: Optional[JobDocument] = Field(
        None, description='Optional snapshot of the document metadata at job creation.'
    )

    # Timestamps
    date_created: datetime = Field(
        ..., alias='dateCreated', description='Timestamp when the job was created.'
    )
    date_updated: datetime = Field(
        ..., alias='dateUpdated', description='Timestamp when the job was last updated.'
    )

    class Config:
        validate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}

        # This helps with IDE autocompletion for the Union type
        arbitrary_types_allowed = True

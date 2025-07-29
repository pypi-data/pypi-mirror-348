from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field, ConfigDict, field_serializer

from gestell.types.job import Job
from gestell.types.layout import (
    AudioLayout,
    DocumentLayout,
    LayoutType,
    PhotoLayout,
    VideoLayout,
)


class DocumentMetadata(BaseModel):
    """
    File metadata for a document.

    Attributes:
        size (int): File size in bytes.
        pages (int): Number of pages (for paginated documents).
        length (float): Duration in seconds (for audio/video).
    """

    size: int = Field(..., description='File size in bytes.')
    pages: int = Field(..., description='Number of pages (for paginated documents).')
    length: float = Field(..., description='Duration in seconds (for audio/video).')


class Document(BaseModel):
    """
    Represents a document stored within a collection.

    This model includes processing job details, layout information, and file metadata
    for documents of various types (text, images, audio, video).

    Attributes:
        id (str): Unique identifier for the document.
        collection_id (str): Identifier of the parent collection.
        name (str): Human-readable name of the document (e.g., filename).
        type (str): MIME type or custom type label of the document.
        layout_type (LayoutType): The layout parsing strategy applied.
        layout_nodes (int): Number of layout nodes generated during parsing.
        tables (bool): Whether the document contains tables to be parsed.
        instructions (str): Custom instructions or notes for processing.
        job (Optional[Job]): Processing job associated with this document, if any.
        layout (Optional[Union[List[DocumentLayout], List[PhotoLayout],
                List[VideoLayout], List[AudioLayout]]]):
            Parsed layout structure, varying by `layout_type`.
        metadata (Optional[DocumentMetadata]):
            File metadata including size, pages, and duration.
        date_created (datetime): Timestamp when the document was created.
        date_updated (datetime): Timestamp when the document was last updated.
    """

    # Enable alias population (e.g. `collectionId` → `collection_id`)
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description='Unique identifier for the document.')
    collection_id: str = Field(
        ..., alias='collectionId', description='Identifier of the parent collection.'
    )
    name: str = Field(..., description='Human-readable name (e.g., filename).')
    type: str = Field(..., description='MIME type or custom type label.')
    layout_type: LayoutType = Field(
        ..., alias='layoutType', description='Layout parsing strategy applied.'
    )
    layout_nodes: int = Field(
        ..., alias='layoutNodes', description='Number of layout nodes generated.'
    )
    tables: bool = Field(..., description='Whether the document contains tables.')
    instructions: str = Field(..., description='Custom processing instructions.')

    job: Optional[Job] = Field(
        None, description='Processing job associated with this document, if any.'
    )
    layout: Optional[
        Union[
            List[DocumentLayout],
            List[PhotoLayout],
            List[VideoLayout],
            List[AudioLayout],
        ]
    ] = Field(
        None,
        description=(
            'Parsed layout structure, varying by `layout_type`:\n'
            '- `DocumentLayout[]` for text/image docs\n'
            '- `PhotoLayout[]` for images\n'
            '- `VideoLayout[]` for videos\n'
            '- `AudioLayout[]` for audio'
        ),
    )
    metadata: Optional[DocumentMetadata] = Field(
        None,
        description=(
            'File metadata for the document:\n'
            '- `size`: bytes\n'
            '- `pages`: page count\n'
            '- `length`: duration in seconds'
        ),
    )

    date_created: datetime = Field(
        ..., alias='dateCreated', description='Timestamp when created.'
    )
    date_updated: datetime = Field(
        ..., alias='dateUpdated', description='Timestamp when last updated.'
    )

    @field_serializer('date_created', mode='plain')
    def _serialize_date_created(self, dt: datetime, _info) -> str:
        """Serialize `date_created` to ISO 8601 string."""
        return dt.isoformat()

    @field_serializer('date_updated', mode='plain')
    def _serialize_date_updated(self, dt: datetime, _info) -> str:
        """Serialize `date_updated` to ISO 8601 string."""
        return dt.isoformat()
